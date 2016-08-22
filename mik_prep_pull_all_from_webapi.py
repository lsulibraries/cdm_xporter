#! /usr/bin/env python3

import os
import urllib
from lxml import etree as ET
import json

import pull_from_cdm_for_mik as p

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
    write_collection_level_metadata(alias)
    do_root_level_objects(alias)
    do_compound_objects(alias)


def write_collection_level_metadata(alias):
    alias_dir = os.path.join('..', 'Cached_Cdm_files', alias)
    os.makedirs(alias_dir, exist_ok=True)
    if not os.path.isfile('{}/Collection_Metadata.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_metadata(alias),
            alias_dir,
            'Collection_Metadata')
    if not os.path.isfile('{}/Collection_TotalRecs.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_total_recs(alias),
            alias_dir,
            'Collection_TotalRecs')
    if not os.path.isfile('{}/Collection_Fields.json'.format(alias_dir)):
        p.write_json_to_file(
            p.retrieve_collection_fields_json(alias),
            alias_dir,
            'Collection_Fields')
    if not os.path.isfile('{}/Collection_Fields.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_fields_xml(alias),
            alias_dir,
            'Collection_Fields')


def do_root_level_objects(alias):
    alias_dir = os.path.join('..', 'Cached_Cdm_files', alias)
    num_root_objects = count_root_objects(alias_dir)
    chunk_size = 100
    num_chunks = (num_root_objects // chunk_size) + 1
    for num in range(num_chunks):
        starting_position = (num * chunk_size) + 1
        write_chunk_of_elems_in_collection(alias, starting_position, chunk_size)

    all_root_pointers_filetypes = find_root_pointers_filetypes(alias_dir)
    for pointer, filetype in all_root_pointers_filetypes:
        process_root_level_objects(alias, pointer, filetype)


def count_root_objects(alias_dir):
    total_recs_etree = ET.parse(os.path.join(alias_dir, 'Collection_TotalRecs.xml'))
    return int(total_recs_etree.xpath('.//total')[0].text)


def write_chunk_of_elems_in_collection(alias, starting_position, chunk_size):
    alias_dir = os.path.join('..', 'Cached_Cdm_files', alias)
    if not os.path.isfile('{}/Elems_in_Collection_{}.json'.format(alias_dir, starting_position)):
        p.write_json_to_file(
            p.retrieve_elems_in_collection(alias, starting_position, chunk_size, 'json'),
            alias_dir,
            'Elems_in_Collection_{}'.format(starting_position))
    if not os.path.isfile('{}/Elems_in_Collection_{}.xml'.format(alias_dir, starting_position)):
        p.write_xml_to_file(
            p.retrieve_elems_in_collection(alias, starting_position, chunk_size, 'xml'),
            alias_dir,
            'Elems_in_Collection_{}'.format(starting_position))


def find_root_pointers_filetypes(alias_dir):
    Elems_filelist = [file for file in os.listdir(alias_dir)
                      if 'Elems_in_Collection' in file and
                      '.xml' in file]
    pointers_filetypes = []
    for file in Elems_filelist:
        elems_in_col_etree = ET.parse(os.path.join(alias_dir, file))
        for single_record in elems_in_col_etree.findall('.//record'):
            pointer = single_record.find('dmrecord').text or single_record.find('pointer').text
            filetype = single_record.find('filetype').text.lower()
            if pointer and filetype:
                pointers_filetypes.append((pointer, filetype))
    return pointers_filetypes


def process_root_level_objects(alias, pointer, filetype):
    alias_dir = os.path.join('..', 'Cached_Cdm_files', alias)
    cpd_dir = os.path.join(alias_dir, 'Cpd')
    if filetype != 'cpd':
        write_metadata(alias_dir, alias, pointer, 'simple')
        process_binary(alias_dir, alias, pointer, filetype)
    elif filetype == 'cpd':
        write_metadata(cpd_dir, alias, pointer, 'cpd')


def write_metadata(target_dir, alias, pointer, simple_or_cpd):
    print(pointer)
    if not os.path.isfile('{}/{}.xml'.format(target_dir, pointer)):
        xml_text = p.retrieve_item_metadata(alias, pointer, 'xml')
        if is_it_a_404_xml(xml_text):
            broken_pointers.add((alias, pointer))
        else:
            p.write_xml_to_file(xml_text, target_dir, pointer)
            print('wrote xml_text')

    if not os.path.isfile('{}/{}.json'.format(target_dir, pointer)):
        json_text = p.retrieve_item_metadata(alias, pointer, 'json')
        if is_it_a_404_json(json_text):
            broken_pointers.add((alias, pointer))
        else:
            p.write_json_to_file(json_text, target_dir, pointer)
        print('wrote json_text')

    if not os.path.isfile('{}/{}_parent.xml'.format(target_dir, pointer)):
        xml_parent_text = p.retrieve_parent_info(alias, pointer, 'xml')
        if is_it_a_404_xml(xml_parent_text):
            broken_pointers.add((alias, pointer))
        else:
            p.write_xml_to_file(xml_parent_text, target_dir, '{}_parent'.format(pointer))
        print('wrote xml_parent_text')

    if not os.path.isfile('{}/{}_parent.json'.format(target_dir, pointer)):
        json_parent_text = p.retrieve_parent_info(alias, pointer, 'json')
        if is_it_a_404_json(json_parent_text):
            broken_pointers.add((alias, pointer))
        else:
            p.write_json_to_file(json_parent_text, target_dir, '{}_parent'.format(pointer))
        print('wrote json_parent_text')

    if simple_or_cpd == 'cpd':
        if not os.path.isfile('{}/{}_cpd.xml'.format(target_dir, pointer)):
            index_file_text = p.retrieve_compound_object(alias, pointer)
            if is_it_a_404_xml(index_file_text):
                broken_pointers.add((alias, pointer))
            else:
                p.write_xml_to_file(index_file_text, target_dir, '{}_cpd'.format(pointer))
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


def process_binary(target_dir, alias, pointer, filetype):
    return
    # item_xml_filepath = '{}/{}.xml'.format(target_dir, pointer)
    # item_etree = ET.parse(item_xml_filepath)
    # if item_etree.find('find') is not None:    # i.e., does this pointer have a file
    if not os.path.isfile('{}/{}.{}'.format(target_dir, pointer, filetype)):
        try:
            p.write_binary_to_file(
                p.retrieve_binary(alias, pointer),
                target_dir,
                pointer,
                filetype)
            print('wrote', alias, pointer, filetype)
        except urllib.error.HTTPError:
            print('HTTP error caught on binary')
            unavailable_binaries.append((alias, pointer, filetype))


def do_compound_objects(alias):
    cpd_dir = os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd')
    if os.path.isdir(cpd_dir):
        index_file_list = [i for i in os.listdir(cpd_dir)
                           if os.path.isfile(os.path.join(cpd_dir, i)) and
                           '_cpd.xml' in i]
        for file in index_file_list:
            write_child_data(alias, file)


def write_child_data(alias, index_file):
    cpd_pointer = index_file.split('_')[0]
    cpd_object_dir = os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd', cpd_pointer)
    index_file_path = os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd', index_file)
    children_elements_list = ET.parse(index_file_path).findall('.//pageptr')

    if has_pdfpage_elems(children_elements_list):
        try_to_get_a_hidden_pdf_at_root_of_cpd(alias, index_file)
        return False        # abort processing this psuedo-compound's children

    for child in children_elements_list:
        child_pointer = child.text
        write_metadata(cpd_object_dir, alias, child_pointer, 'simple')
        try:
            child_filetype = parse_binary_original_filetype(cpd_object_dir, child_pointer)
        except OSError:
            broken_pointers.add((alias, child_pointer))
            continue
        process_binary(cpd_object_dir, alias, child_pointer, child_filetype)


def try_to_get_a_hidden_pdf_at_root_of_cpd(alias, index_file):
    cpd_dir = os.path.join('..', 'Cached_Cdm_files', alias, 'Cpd')
    xml_file = "{}.xml".format(index_file.split('_')[0])
    root_cpd_etree = ET.parse(os.path.join(cpd_dir, xml_file))
    pointer = root_cpd_etree.findall('.//dmrecord')[0].text
    filetype = root_cpd_etree.findall('.//format')[0].text.lower()
    if not os.path.isfile('{}/{}.{}'.format(cpd_dir, pointer, filetype)):
        try:
            binary = p.retrieve_binary(alias, pointer)
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
            print('{} {}_cpd.xml isnt a binary at root'.format(cpd_dir, pointer))
        except UnicodeDecodeError:
            p.write_binary_to_file(binary, cpd_dir, pointer, filetype)
            print(cpd_dir, pointer, 'wrote root binary')


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
    # for alias in ('p120701coll17',):
    for alias in ('p120701coll17',):
        broken_pointers = set()
        main(alias)
        incomplete_collection.append('{} {}'.format(alias, broken_pointers))
    print('incomplete:', incomplete_collection)
    print('unavailable binaries:', unavailable_binaries)

    """ Get all collections' metadata/binaries """

    # repo_dir = '../Cached_Cdm_files'
    # if not os.path.isfile(os.path.join(repo_dir, 'Collections_List.xml')):
    #     coll_list_txt = p.retrieve_collections_list()
    #     p.write_xml_to_file(coll_list_txt, repo_dir, 'Collections_List')
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
