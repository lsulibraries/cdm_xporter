#! /usr/bin/env python3

import os
import lxml.etree as etree
from retrying import retry

import pull_from_cdm_for_mik as p


def read_file(filename):
    with open(filename) as f:
        return f.read()


# @retry(wait_random_min=1000, wait_random_max=20000)
def just_so_i_can_call_it(alias):
    repo_dir = '{}/{}'.format(os.getcwd(), 'Cached_Cdm_files')
    alias_dir = '{}/{}'.format(repo_dir, alias)

    os.makedirs(alias_dir, exist_ok=True)

    if not os.path.isfile('{}/Collection_Metadata.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_metadata(alias),
            alias,
            'Collection_Metadata')

    if not os.path.isfile('{}/Collection_TotalRecs.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_total_recs(alias),
            alias,
            'Collection_TotalRecs')

    if not os.path.isfile('{}/Collection_Fields.json'.format(alias_dir)):
        collection_fields_json = p.retrieve_collection_fields_json(alias)
        p.write_json_to_file(
            collection_fields_json,
            alias,
            'Collection_Fields')

    if not os.path.isfile('{}/Collection_Fields.xml'.format(alias_dir)):
        collection_fields_xml = p.retrieve_collection_fields_xml(alias)
        p.write_xml_to_file(
            collection_fields_xml,
            alias,
            'Collection_Fields')
    else:
        collection_fields_xml = read_file(
            '{}/Collection_Fields.xml'.format(alias_dir))

    total_recs_etree = etree.fromstring(bytes(bytearray(p.retrieve_collection_total_recs(alias), encoding='utf-8')))
    num_of_pointers = int(total_recs_etree.xpath('.//total')[0].text)
    groups_of_100 = (num_of_pointers // 100) + 1

    for num in range(groups_of_100):
        starting_pointer = (num * 100) + 1
        if not os.path.isfile('{}/Elems_in_Collection_{}.xml'.format(alias_dir, starting_pointer)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            xml_elems_in_coll = p.retrieve_elems_xml(alias, fields_to_retrieve, starting_pointer)
            p.write_xml_to_file(
                xml_elems_in_coll,
                alias,
                'Elems_in_Collection_{}'.format(starting_pointer))

        elems_in_coll_tree = etree.parse(
            '{}/Elems_in_Collection_{}.xml'.format(alias_dir, starting_pointer))

        if not os.path.isfile('{}/Elems_in_Collection_{}.json'.format(alias_dir, starting_pointer)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            json_elems_in_coll = p.retrieve_elems_json(alias, fields_to_retrieve, starting_pointer)
            p.write_json_to_file(
                json_elems_in_coll,
                alias,
                'Elems_in_Collection_{}'.format(starting_pointer))

        """ Careful method of getting each object contentdm says is in a collection"""
        pointers_filetypes = [(single_record.find('dmrecord').text,
                               single_record.find('filetype').text,
                               ) for single_record in elems_in_coll_tree.findall('.//record')]

        for pointer, filetype in pointers_filetypes:
            if not pointer:
                continue  # skips file if a derivative -- only gets original versions

            if filetype != 'cpd':

                if not os.path.isfile('{}/{}.json'.format(alias_dir, pointer)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, alias, pointer)

                if not os.path.isfile('{}/{}.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, alias, pointer)

                if not os.path.isfile('{}/{}_parent.xml'.format(alias_dir, pointer)):
                    parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                    p.write_xml_to_file(parent_xml, alias, '{}_parent'.format(pointer))

                if not os.path.isfile('{}/{}_parent.json'.format(alias_dir, pointer)):
                    parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                    p.write_json_to_file(parent_json, alias, '{}_parent'.format(pointer))

                item_xml_filepath = '{}/{}.xml'.format(alias_dir, pointer)
                item_etree = etree.parse(item_xml_filepath)
                if item_etree.find('find') is not None:  # "find" is contentdm's abbr for 'file name'
                    if not os.path.isfile('{}/{}.{}'.format(alias_dir, pointer, filetype)):
                        binary = p.retrieve_binaries(alias, pointer, "_")
                        p.write_binary_to_file(binary, alias, pointer, filetype)
                        print('wrote', alias, pointer, filetype)

            elif filetype == 'cpd':
                os.makedirs('{}/Cpd'.format(alias_dir), exist_ok=True)

                if not os.path.isfile('{}/Cpd/{}.json'.format(alias_dir, pointer)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, '{}/Cpd'.format(alias), pointer)

                if not os.path.isfile('{}/Cpd/{}.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), pointer)

                if not os.path.isfile('{}/Cpd/{}_parent.xml'.format(alias_dir, pointer)):
                    parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                    p.write_xml_to_file(parent_xml, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

                if not os.path.isfile('{}/Cpd/{}_parent.json'.format(alias_dir, pointer)):
                    parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                    p.write_json_to_file(parent_json, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

                item_xml_filepath = '{}/Cpd/{}.xml'.format(alias_dir, pointer)
                item_etree = etree.parse(item_xml_filepath)

                if not os.path.isfile('{}/Cpd/{}_cpd.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_compound_object(alias, pointer)
                    p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), '{}_cpd'.format(pointer))

            else:
                print('{} {}, not pointer filetype'.format(pointer, filetype))

    if 'Cpd' in os.listdir(alias_dir):
        for file in os.listdir(os.path.join(alias_dir, 'Cpd')):
            if '_cpd.xml' in file:
                cpd_pointer = file.split('_')[0]
                small_etree = etree.parse(os.path.join(alias_dir, 'Cpd', file))
                subpointer_list = small_etree.findall('.//pageptr')
                file_element = subpointer_list[0].getparent().xpath('./pagefile')
                if file_element and 'pdfpage' in file_element[0].text:
                    continue  # we don't want pdfpage objects
                os.makedirs('{}/Cpd/{}'.format(alias_dir, cpd_pointer), exist_ok=True)
                for elem in subpointer_list:
                    simple_pointer = elem.text
                    # if alias == 'LSU_SCE' and simple_pointer in ('269', '308', '258', '261'):
                    #     continue    # skipping known bad objects

                    if not os.path.isfile('{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                        item_xml = p.retrieve_item_metadata(alias, simple_pointer, 'xml')
                        p.write_xml_to_file(item_xml, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                    else:
                        item_xml = read_file(
                            '{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                        item_json = p.retrieve_item_metadata(alias, simple_pointer, 'json')
                        p.write_json_to_file(item_json, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}_parent.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                        parent_xml = p.retrieve_parent_info(alias, simple_pointer, 'xml')
                        p.write_xml_to_file(parent_xml, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}_parent.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                        parent_json = p.retrieve_parent_info(alias, simple_pointer, 'json')
                        p.write_json_to_file(parent_json, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))


                    simple_etree = etree.fromstring(bytes(bytearray(item_xml, encoding='utf-8')))
                    orig_filename = simple_etree.find('find').text
                    simple_filetype = os.path.splitext(orig_filename)[-1].replace('.', '')
                    if not os.path.isfile('{}/Cpd/{}/{}.{}'.format(alias_dir, cpd_pointer, simple_pointer, simple_filetype)):
                        binary = p.retrieve_binaries(alias, simple_pointer, "arbitary")
                        simple_filepath = 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer)
                        p.write_binary_to_file(binary, alias, simple_filepath, simple_filetype)
                        print('wrote', alias, cpd_pointer, simple_pointer, simple_filetype)

if __name__ == '__main__':
    """ Call just one collection, retrieve all metadata """
    just_so_i_can_call_it('AAW')

    """ Call all collections, retrieve all metadata """

    # coll_list_txt = p.retrieve_collections_list()
    # p.write_xml_to_file(coll_list_txt, '.', 'Collections_List')
    # coll_list_xml = etree.fromstring(bytes(bytearray(coll_list_txt, encoding='utf-8')))
    # not_all_binaries = []
    # for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
    #     try:
    #         print(alias)
    #         just_so_i_can_call_it(alias)
    #     except:
    #         not_all_binaries.append(alias)
    #         print('oops')
    # print(not_all_binaries)
