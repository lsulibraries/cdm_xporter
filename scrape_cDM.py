#! /usr/bin/env python3

import os
import urllib
from lxml import etree as ET
import json

import cDM_api_calls as cDM

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


def main(alias):
    print(alias)
    alias_source_tree = [i for i in os.walk(os.path.realpath(os.path.join('..', 'Cached_Cdm_files', alias)))]
    write_collection_level_metadata(alias, alias_source_tree)
    do_root_level_objects(alias, alias_source_tree)
    do_compound_objects(alias, alias_source_tree)


def write_collection_level_metadata(alias, alias_source_tree):
    # searching our directory tree for the path ending in our alias.
    path, files = [(path, files) for path, dirs, files in alias_source_tree if os.path.split(path)[-1] == alias][0]
    if 'Collection_TotalRecs.xml' not in files:
        cDM.write_xml_to_file(cDM.retrieve_collection_total_recs(alias), path, 'Collection_TotalRecs')
    if 'Collection_Metadata.xml' not in files:
        cDM.write_xml_to_file(cDM.retrieve_collection_metadata(alias), path, 'Collection_Metadata')
    if 'Collection_Fields.json' not in files:
        cDM.write_json_to_file(cDM.retrieve_collection_fields_json(alias), path, 'Collection_Fields')
    if 'Collection_Fields.xml' not in files:
        cDM.write_xml_to_file(cDM.retrieve_collection_fields_xml(alias), path, 'Collection_Fields')


def do_root_level_objects(alias, alias_source_tree):
    alias_dir = os.path.join('..', 'Cached_Cdm_files', alias)
    num_root_objects = count_root_objects(alias_dir)
    chunksize = 100
    num_chunks = (num_root_objects // chunksize) + 1
    for num in range(num_chunks):
        starting_position = (num * chunksize) + 1
        write_chunk_of_elems_in_collection(alias, starting_position, chunksize, alias_source_tree)

    all_root_pointers_filetypes = find_root_pointers_filetypes(alias_source_tree)
    for pointer, filetype in all_root_pointers_filetypes:
        process_root_level_objects(alias, pointer, filetype, alias_source_tree)


def count_root_objects(alias_dir):
    total_recs_etree = ET.parse(os.path.join(alias_dir, 'Collection_TotalRecs.xml'))
    return int(total_recs_etree.xpath('.//total')[0].text)


def write_chunk_of_elems_in_collection(alias, pos, chunksize, alias_source_tree):
    path, files = [(path, files) for path, dirs, files in alias_source_tree if os.path.split(path)[-1] == alias][0]
    if 'Elems_in_Collection_{}.json'.format(pos) not in files:
        cDM.write_json_to_file(
            cDM.retrieve_elems_in_collection(alias, pos, chunksize, 'json'),
            path,
            'Elems_in_Collection_{}'.format(pos))
    if 'Elems_in_Collection_{}.xml'.format(pos) not in files:
        cDM.write_xml_to_file(
            cDM.retrieve_elems_in_collection(alias, pos, chunksize, 'xml'),
            path,
            'Elems_in_Collection_{}'.format(pos))


def find_root_pointers_filetypes(alias_source_tree):
    path, files = [(path, files) for path, dirs, files in alias_source_tree if os.path.split(path)[-1] == alias][0]
    Elems_filelist = [file for file in files if 'Elems_in_Collection' in file and '.xml' in file]
    pointers_filetypes = []
    for file in Elems_filelist:
        elems_in_col_etree = ET.parse(os.path.join(path, file))
        for single_record in elems_in_col_etree.findall('.//record'):
            pointer = single_record.find('dmrecord').text or single_record.find('pointer').text
            filetype = single_record.find('filetype').text.lower()
            if pointer and filetype:
                pointers_filetypes.append((pointer, filetype))
    return pointers_filetypes


def process_root_level_objects(alias, pointer, filetype, alias_source_tree):
    alias_dir = os.path.realpath(os.path.join('..', 'Cached_Cdm_files', alias))
    cpd_dir = os.path.join(alias_dir, 'Cpd')
    if filetype != 'cpd':
        write_metadata(alias_dir, alias, pointer, alias_source_tree, 'simple')
        process_binary(alias_dir, alias, pointer, filetype, alias_source_tree)
    elif filetype == 'cpd':
        write_metadata(cpd_dir, alias, pointer, alias_source_tree, 'cpd')


def write_metadata(target_dir, alias, pointer, alias_source_tree, simple_or_cpd):
    print(pointer)
    path, files = [(path, files) for path, dirs, files in alias_source_tree if target_dir == path][0]

    if "{}.xml".format(pointer) not in files:
        xml_text = cDM.retrieve_item_metadata(alias, pointer, 'xml')
        if is_it_a_404_xml(xml_text):
            broken_pointers.add((alias, pointer))
        else:
            cDM.write_xml_to_file(xml_text, target_dir, pointer)
            print('wrote xml_text')

    if '{}.json'.format(pointer) not in files:
        json_text = cDM.retrieve_item_metadata(alias, pointer, 'json')
        if is_it_a_404_json(json_text):
            broken_pointers.add((alias, pointer))
        else:
            cDM.write_json_to_file(json_text, target_dir, pointer)
        print('wrote json_text')

    if '{}_parent.xml'.format(pointer) not in files:
        xml_parent_text = cDM.retrieve_parent_info(alias, pointer, 'xml')
        if is_it_a_404_xml(xml_parent_text):
            broken_pointers.add((alias, pointer))
        else:
            cDM.write_xml_to_file(xml_parent_text, target_dir, '{}_parent'.format(pointer))
        print('wrote xml_parent_text')

    if '{}_parent.json'.format(pointer) not in files:
        json_parent_text = cDM.retrieve_parent_info(alias, pointer, 'json')
        if is_it_a_404_json(json_parent_text):
            broken_pointers.add((alias, pointer))
        else:
            cDM.write_json_to_file(json_parent_text, target_dir, '{}_parent'.format(pointer))
        print('wrote json_parent_text')

    if simple_or_cpd == 'cpd':
        if '{}_cpd.xml'.format(pointer) not in files:
            index_file_text = cDM.retrieve_compound_object(alias, pointer)
            if is_it_a_404_xml(index_file_text):
                broken_pointers.add((alias, pointer))
            else:
                cDM.write_xml_to_file(index_file_text, target_dir, '{}_cpd'.format(pointer))
            print('wrote xml_index_file_text')


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


def process_binary(target_dir, alias, pointer, filetype, alias_source_tree):
    path, files = [(path, files) for path, dirs, files in alias_source_tree if target_dir == path][0]

    if '{}.{}'.format(pointer, filetype) not in files:
        try:
            cDM.write_binary_to_file(
                cDM.retrieve_binary(alias, pointer),
                target_dir,
                pointer,
                filetype)
            print('wrote', alias, pointer, filetype)
        except urllib.error.HTTPError:
            print('HTTP error caught on binary')
            unavailable_binaries.append((alias, pointer, filetype))


def do_compound_objects(alias, alias_source_tree):
    index_files = [file for path, dirs, files in alias_source_tree for file in files if "_cpd.xml" in file]
    for file in index_files:
        write_child_data(alias, file, alias_source_tree)


def write_child_data(alias, index_file, alias_source_tree):
    cpd_pointer = index_file.split('_')[0]
    cpd_object_dir = os.path.realpath(os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd', cpd_pointer))
    index_file_path = os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd', index_file)
    children_elements_list = ET.parse(index_file_path).findall('.//pageptr')

    if has_pdfpage_elems(children_elements_list):
        try_to_get_a_hidden_pdf_at_root_of_cpd(alias, index_file, alias_source_tree)
        return False        # abort processing this psuedo-compound's children

    for child in children_elements_list:
        child_pointer = child.text
        write_metadata(cpd_object_dir, alias, child_pointer, alias_source_tree, 'simple')
        try:
            child_filetype = parse_binary_original_filetype(cpd_object_dir, child_pointer)
        except OSError:
            broken_pointers.add((alias, child_pointer))
            continue
        process_binary(cpd_object_dir, alias, child_pointer, child_filetype, alias_source_tree)


def try_to_get_a_hidden_pdf_at_root_of_cpd(alias, index_file, alias_source_tree):
    path, files = [(path, files) for path, dirs, files in alias_source_tree if index_file in files][0]
    xml_file = "{}.xml".format(index_file.split('_')[0])
    root_cpd_etree = ET.parse(os.path.join(path, xml_file))
    pointer = root_cpd_etree.findall('.//dmrecord')[0].text
    filetype = root_cpd_etree.findall('.//format')[0].text.lower()
    if '{}.{}'.format(pointer, filetype) not in files:
        try:
            binary = cDM.retrieve_binary(alias, pointer)
        except urllib.error.HTTPError:
            print('HTTP error caught on binary')
            unavailable_binaries.append((alias, pointer, filetype))
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

    """ Get specific collections' metadata/binaries """
    unavailable_binaries = []
    incomplete_collection = []
    for alias in ('p120701coll17',):
        broken_pointers = set()
        main(alias)
        incomplete_collection.append('{} {}'.format(alias, broken_pointers))
    print('Incompletes:\n'.format('\n\t'.join(i for i in incomplete_collection)))
    print('Unavailable binaries:\n\t{}'.format('\n\t'.join(i for i in unavailable_binaries)))

    """ Get all collections' metadata/binaries """

    # repo_dir = '../Cached_Cdm_files'
    # if not os.path.isfile(os.path.join(repo_dir, 'Collections_List.xml')):
    #     coll_list_txt = cDM.retrieve_collections_list()
    #     cDM.write_xml_to_file(coll_list_txt, repo_dir, 'Collections_List')
    # coll_list_xml = ET.parse(os.path.join(repo_dir, 'Collections_List.xml'))
    # not_all_binaries = []
    # for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
    #     broken_pointers = set()
    #     if alias in WE_DONT_MIGRATE:
    #         continue
    #     # try:
    #     #     print('{} '.format(alias) * 10)
    #     main(alias)
    #     # except:
    #     #     not_all_binaries.append((alias, broken_pointers))
    #     print(alias)
    #     print(broken_pointers)
    # print(not_all_binaries)
