#! /usr/bin/env python3

import os
import urllib
from lxml import etree as ET
import json

import cDM_api_calls as cDM


# weird bug where it won't get objects the first pass.  Requires two runs, for any collection with no previous data.

WE_DONT_MIGRATE = {'p16313coll70', 'p120701coll11', 'LSUHSCS_JCM', 'UNO_SCC', 'p15140coll36', 'p15140coll57',
                   'p15140coll13', 'p15140coll11', 'p16313coll32', 'p16313coll49', 'p16313coll50',
                   'p16313coll90', 'p120701coll14', 'p120701coll20', 'p120701coll21', 'DUBLIN2',
                   'HHN', 'p15140coll55', 'NOD', 'WIS', 'p16313coll55', 'LOU_RANDOM', 'p120701coll11',
                   'p16313coll67', 'AMA', 'HTU', 'p15140coll3', 'p15140coll15', 'p15140coll25',
                   'p15140coll29', 'p15140coll34', 'p15140coll37', 'p15140coll38', 'p15140coll39',
                   'p15140coll40', 'p15140coll45', 'p15140coll47', 'p15140coll58', 'p16313coll4',
                   'p16313coll6', 'p16313coll11', 'p16313coll12', 'p16313coll13', 'p16313coll14',
                   'p16313coll15', 'p16313coll16', 'p16313coll29', 'p16313coll27', 'p16313coll30',
                   'p16313coll33', 'p16313coll37', 'p16313coll38', 'p16313coll39', 'p16313coll41',
                   'p16313coll42', 'p16313coll46', 'p16313coll47', 'p16313coll53', 'p16313coll59',
                   'p16313coll63', 'p16313coll64', 'p16313coll66', 'p16313coll68', 'p16313coll71',
                   'p16313coll73', 'p16313coll75', 'p16313coll78', 'p16313coll84',
                   'p15140coll32', 'p16313coll82', 'p120701coll6', 'p267101coll4',
                   'p16313coll44', 'p16313coll88', 'p16313coll94', 'JSN', 'p15140coll24',
                   'p15140coll9', 'p15140coll59', 'p16313coll40', 'p15140coll53', 'p16313coll97',
                   'p16313coll18', 'p15140coll33', 'LST', 'MPF', 'p15140coll2', }


"""
"alias" is contentDM's term for collections.
"pointer" is contentDM's term for objects.

An alias will have pointers at its root, which may be simple or compound objects.
A compound object will have simple objects at its root.

This script outputs a collection as:
Cachec_Cdm_files-
    Alias-
        Pointer1
        Pointer2
        Pointer3-
            Pointer4
            Pointer5
        Pointer6
(where pointers 1, 2, and 6 are simple objects.  Pointers 4 and 5 are the simple object children
 of compound object pointer 3).
"""


class ScrapeAlias():
    def __init__(self, alias):
        self.alias = alias
        self.alias_dir = None
        self.unavailable_metadata = set()
        self.unavailable_binaries = set()
        self.compound_parents = []
        # it's notable that tree_snapshot gets created after the collection level metadata is written
        # therefore it will be empty until just after the Elems_in_Collection's are written.
        self.tree_snapshot = []

    def main(self):
        print(self.alias)
        self.alias_dir = os.path.realpath('../Cached_Cdm_files/{}/'.format(self.alias))
        self.do_collection_level_metadata()
        self.do_root_level_objects()
        self.do_compound_objects()

    def do_collection_level_metadata(self):
        path = self.alias_dir
        os.makedirs(path, exist_ok=True)
        files = [i for i in os.listdir(path)]
        if 'Collection_TotalRecs.xml' not in files:
            cDM.write_xml_to_file(
                cDM.retrieve_collection_total_recs(alias),
                path,
                'Collection_TotalRecs')
        if 'Collection_Metadata.xml' not in files:
            cDM.write_xml_to_file(
                cDM.retrieve_collection_metadata(alias),
                path,
                'Collection_Metadata')
        if 'Collection_Fields.json' not in files:
            cDM.write_json_to_file(cDM.retrieve_collection_fields_json(alias),
                path,
                'Collection_Fields')
        if 'Collection_Fields.xml' not in files:
            cDM.write_xml_to_file(cDM.retrieve_collection_fields_xml(alias),
                path,
                'Collection_Fields')

    def do_root_level_objects(self):
        num_root_objects = self.count_root_objects()
        chunksize = 100
        num_chunks = (num_root_objects // chunksize) + 1
        for num in range(num_chunks):
            starting_position = (num * chunksize) + 1
            self.write_chunk_of_elems_in_collection(starting_position, chunksize)
        self.tree_snapshot = [i for i in os.walk(self.alias_dir)]
        for pointer, filetype in self.find_root_pointers_filetypes():
            self.process_root_level_objects(pointer, filetype)

    def count_root_objects(self):
        total_recs_etree = ET.parse(os.path.join(self.alias_dir, 'Collection_TotalRecs.xml'))
        return int(total_recs_etree.xpath('.//total')[0].text)

    def write_chunk_of_elems_in_collection(self, starting_position, chunksize):
        path = self.alias_dir
        files = [i for i in os.listdir(path)]
        if 'Elems_in_Collection_{}.json'.format(starting_position) not in files:
            cDM.write_json_to_file(
                cDM.retrieve_elems_in_collection(self.alias, starting_position, chunksize, 'json'),
                path,
                'Elems_in_Collection_{}'.format(starting_position))
        if 'Elems_in_Collection_{}.xml'.format(starting_position) not in files:
            cDM.write_xml_to_file(
                cDM.retrieve_elems_in_collection(alias, starting_position, chunksize, 'xml'),
                path,
                'Elems_in_Collection_{}'.format(starting_position))

    def find_root_pointers_filetypes(self):
        path = self.alias_dir
        files = [file for file in os.listdir(path) if 'Elems_in_Collection' in file and '.xml' in file]
        pointers_filetypes = []
        for file in files:
            elems_in_col_etree = ET.parse(os.path.join(path, file))
            for single_record in elems_in_col_etree.findall('.//record'):
                pointer = single_record.find('dmrecord').text or single_record.find('pointer').text
                filetype = single_record.find('filetype').text.lower()
                if pointer and filetype:
                    pointers_filetypes.append((pointer, filetype))
        return pointers_filetypes

    def process_root_level_objects(self, pointer, filetype):
        if filetype != 'cpd':
            self.write_metadata(self.alias_dir, pointer, 'simple')
            self.process_binary(self.alias_dir, pointer, filetype)
        elif filetype == 'cpd':
            cpd_path = os.path.join(self.alias_dir, 'Cpd')
            os.makedirs(cpd_path, exist_ok=True)
            self.write_metadata(cpd_path, pointer, 'cpd')
            self.compound_parents.append(pointer)

    def write_metadata(self, target_dir, pointer, simple_or_cpd):
        # checks presence of file before calling to contentDM or overwriting file
        # there can be up to 4000 files checked here per alias,
        # so it is useful to take a snapshot of the directory tree beforehand,
        # instead of reading from the harddrive for each file.
        files = [file for path, dirs, files in self.tree_snapshot for file in files if target_dir == path]

        if "{}.xml".format(pointer) not in files:
            xml_text = cDM.retrieve_item_metadata(self.alias, pointer, 'xml')
            if is_it_a_404_xml(xml_text):
                self.unavailable_metadata.add(pointer)
            else:
                cDM.write_xml_to_file(xml_text, target_dir, pointer)
                print(self.alias, pointer, 'wrote xml_text')

        if '{}.json'.format(pointer) not in files:
            json_text = cDM.retrieve_item_metadata(self.alias, pointer, 'json')
            if is_it_a_404_json(json_text):
                self.unavailable_metadata.add(pointer)
            else:
                cDM.write_json_to_file(json_text, target_dir, pointer)
            print(self.alias, pointer, 'wrote json_text')

        if '{}_parent.xml'.format(pointer) not in files:
            xml_parent_text = cDM.retrieve_parent_info(self.alias, pointer, 'xml')
            if is_it_a_404_xml(xml_parent_text):
                self.unavailable_metadata.add(pointer)
            else:
                cDM.write_xml_to_file(xml_parent_text, target_dir, '{}_parent'.format(pointer))
            print(self.alias, pointer, 'wrote xml_parent_text')

        if '{}_parent.json'.format(pointer) not in files:
            json_parent_text = cDM.retrieve_parent_info(self.alias, pointer, 'json')
            if is_it_a_404_json(json_parent_text):
                self.unavailable_metadata.add(pointer)
            else:
                cDM.write_json_to_file(json_parent_text, target_dir, '{}_parent'.format(pointer))
            print(self.alias, pointer, 'wrote json_parent_text')

        if simple_or_cpd == 'cpd':
            if '{}_cpd.xml'.format(pointer) not in files:
                index_file_text = cDM.retrieve_compound_object(self.alias, pointer)
                if is_it_a_404_xml(index_file_text):
                    self.unavailable_metadata.add(pointer)
                else:
                    cDM.write_xml_to_file(index_file_text, target_dir, '{}_cpd'.format(pointer))
                print(self.alias, pointer, 'wrote xml_index_file_text')

    def process_binary(self, target_dir, pointer, filetype):
        files = [file for root, dirs, files in self.tree_snapshot for file in files if target_dir == root]

        if '{}.{}'.format(pointer, filetype) not in files:
            try:
                cDM.write_binary_to_file(
                    cDM.retrieve_binary(self.alias, pointer),
                    target_dir,
                    pointer,
                    filetype)
                print('wrote', self.alias, pointer, filetype)
            except urllib.error.HTTPError:
                print(self.alias, pointer, 'HTTP error caught on binary')
                self.unavailable_binaries.add((pointer, filetype))

    def do_compound_objects(self):
        for parent_pointer in self.compound_parents:
            os.makedirs(os.path.join(self.alias_dir, 'Cpd', parent_pointer), exist_ok=True)
            self.write_child_data(parent_pointer)

    def write_child_data(self, parent_pointer):
        index_filename = '{}_cpd.xml'.format(parent_pointer)
        index_filepath = os.path.join(self.alias_dir, 'Cpd', index_filename)
        children_pointers_list = ET.parse(index_filepath).findall('.//pageptr')

        if has_pdfpage_elems(children_pointers_list):
            self.try_to_get_a_hidden_pdf_at_root_of_cpd(index_filename)
            return False        # Psuedo-compound pdf object -- skip processing its children.

        child_dir = os.path.realpath(os.path.join(self.alias_dir, 'Cpd', parent_pointer))
        for child in children_pointers_list:
            child_pointer = child.text
            self.write_metadata(child_dir, child_pointer, 'simple')
            try:
                child_filetype = parse_binary_original_filetype(child_dir, child_pointer)
            except OSError:
                self.unavailable_metadata.add(child_pointer)
                continue
            self.process_binary(child_dir, child_pointer, child_filetype)

    def try_to_get_a_hidden_pdf_at_root_of_cpd(self, index_file):
        path = os.path.join(self.alias_dir, 'Cpd')
        sibling_files = [file for root, dirs, files in self.tree_snapshot for file in files if index_file in files]
        xml_file = "{}.xml".format(index_file.split('_')[0])
        root_cpd_etree = ET.parse(os.path.join(path, xml_file))
        pointer = root_cpd_etree.find('.//dmrecord').text or root_cpd_etree.find('.//pointer').text
        filetype = root_cpd_etree.find('.//format').text
        if filetype:
            filetype = filetype.lower()
        else:
            filetype = 'pdf'
        if '{}.{}'.format(pointer, filetype) not in sibling_files:
            try:
                binary = cDM.retrieve_binary(self.alias, pointer)
            except urllib.error.HTTPError:
                print(self.alias, pointer, 'HTTP error caught on binary')
                self.unavailable_binaries.append((pointer, filetype))
                return
            # in some cases, contentDM gives an xml instead of a binary.
            # it's easier to discern whether something is an xml, than to discern
            # whether its one of millions of types of valid binaries.
            # we're going to try to decode the binary or xml into unicode.
            # if it succeeds, it's an xml & we'll discard it.
            # if it fails, it's a binary, which we'll write to file.
            try:
                binary.decode('utf-8')
                print('{} {}_cpd.xml isnt a binary at root'.format(path, pointer))
            except UnicodeDecodeError:
                cDM.write_binary_to_file(binary, path, pointer, filetype)
                print(path, pointer, 'wrote root binary')


def is_it_a_404_xml(xml_text):
    xmldata = bytes(bytearray(xml_text, encoding='utf-8'))
    element_tree = ET.fromstring(xmldata)
    message_elem = element_tree.xpath('./message')
    if message_elem and message_elem[0].text == 'Requested item not found':
        return True
    return False


def is_it_a_404_json(json_text):
    parsed_json = json.loads(json_text)
    if 'message' in parsed_json and parsed_json['message'] == 'Requested item not found':
        return True
    return False


def has_pdfpage_elems(children_elements_list):
    file_elems = children_elements_list[0].getparent().xpath('./pagefile')
    if file_elems and 'pdfpage' in file_elems[0].text:
        return True
    return False


def parse_binary_original_filetype(folder, pointer):
    filepath = '{}/{}.xml'.format(folder, pointer)
    parsed_etree = ET.parse(filepath)
    orig_name = parsed_etree.find('find').text
    filetype = os.path.splitext(orig_name)[-1].replace('.', '').lower()
    return filetype


if __name__ == '__main__':
    all_unavailable_binaries = dict()
    all_unavailable_metadata = dict()

    """ Get specific collections' metadata/binaries """

    for alias in ('p120701coll17',):
        scrapealias = ScrapeAlias(alias)
        scrapealias.main()
        all_unavailable_metadata[alias] = scrapealias.unavailable_metadata
        all_unavailable_binaries[alias] = scrapealias.unavailable_binaries
    print('\n\nUnavailable metadata:')
    for k, v in all_unavailable_metadata.items():
        if len(v):
            print(k)
            print('\n'.join(i for i in v))
    print('\nUnavailable binaries:')
    for k, v in all_unavailable_binaries.items():
        if len(v):
            print(k)
            print('\n'.join(i for i in v))
    print('\n\n')

    """ Get all collections' metadata/binaries """

    # repo_dir = '../Cached_Cdm_files'
    # if not os.path.isfile(os.path.join(repo_dir, 'Collections_List.xml')):
    #     coll_list_txt = cDM.retrieve_collections_list()
    #     cDM.write_xml_to_file(coll_list_txt, repo_dir, 'Collections_List')
    # coll_list_xml = ET.parse(os.path.join(repo_dir, 'Collections_List.xml'))
    # not_all_binaries = []
    # for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
    #     if alias in WE_DONT_MIGRATE:
    #         continue
    #     main(alias)
    # print('Incompletes:\n'.format('\n\t'.join(i for i in incomplete_collection)))
    # print('Unavailable binaries:\n\t{}'.format('\n\t'.join(i for i in unavailable_binaries)))
