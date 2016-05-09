#! /usr/bin/env python3

import os
import lxml.etree as etree
from retrying import retry
# import urllib.request

# import xmlify
import pull_from_cdm_for_mik as p
# import pull_from_cdm
# import pull_from_hd as p


# alias = 'p16313coll54'  # Mingo Family ...
# alias = 'p16313coll38'  # some collection with non-xml-compliant nicknames
# alias = 'p15140coll44'  # missed pdf at root of compound object
# alias = 'p120701coll15'  # some compound objects - some blocked from download
# alias = 'p15140coll30'   # some compound objects
# alias = 'p16313coll81'   # compounds
# alias = 'LSU_BRT'        # simple and compounds


# alias = 'p15140coll15'  # simple objects
# alias = 'p16313coll47'  # simple objects
# alias = 'p16313coll24'   # simple objects
# alias = 'LSUHSCS_JCM'    # single simple object
# alias = 'LSU_JJA'
# alias = 'LSU_GFM'
# alias = 'p16313coll20'
# alias = 'LSU_MRF'


def read_file(filename):
    with open(filename) as f:
        return f.read()

# @retry(wait_random_min=1000, wait_random_max=20000)
def just_so_i_can_call_it(alias):
    repo_dir = '{}/{}'.format(os.getcwd(), 'Cached_Cdm_files')
    alias_dir = '{}/{}'.format(repo_dir, alias)

    os.makedirs('Cached_Cdm_files/{}'.format(alias), exist_ok=True)

    if 'Collection_Metadata.xml' not in os.listdir(alias_dir):
        p.write_xml_to_file(
            p.retrieve_collection_metadata(alias),
            alias,
            'Collection_Metadata')

    if 'Collection_TotalRecs.xml' not in os.listdir(alias_dir):
        p.write_xml_to_file(
            p.retrieve_collection_total_recs(alias),
            alias,
            'Collection_TotalRecs')

    if 'Collection_Fields.xml' not in os.listdir(alias_dir):
        collection_fields = p.retrieve_collection_fields(alias)
        p.write_xml_to_file(
            collection_fields,
            alias,
            'Collection_Fields')
    else:
        collection_fields = read_file(
            '{}/Cached_Cdm_files/{}/Collection_Fields.xml'.format(os.getcwd(), alias))

    total_recs_etree = etree.fromstring(bytes(bytearray(p.retrieve_collection_total_recs(alias), encoding='utf-8')))
    num_of_pointers = int(total_recs_etree.xpath('.//total')[0].text)
    groups_of_100 = (num_of_pointers // 100) + 1

    for num in range(groups_of_100):
        starting_pointer = (num * 100) + 1
        if 'Elems_in_Collection_{}.xml'.format(starting_pointer) not in os.listdir('{}/Cached_Cdm_files/{}/'.format(os.getcwd(), alias)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            xml_elems_in_coll = p.retrieve_elems_xml(alias, fields_to_retrieve, starting_pointer)
            p.write_xml_to_file(xml_elems_in_coll, alias, 'Elems_in_Collection_{}'.format(starting_pointer))

        elems_in_coll_tree = etree.parse(
            '{}/Cached_Cdm_files/{}/Elems_in_Collection_{}.xml'.format(os.getcwd(), alias, starting_pointer))

        if 'Elems_in_Collection_{}.json'.format(starting_pointer) not in os.listdir('{}/Cached_Cdm_files/{}/'.format(os.getcwd(), alias)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            json_elems_in_coll = p.retrieve_elems_json(alias, fields_to_retrieve, starting_pointer)
            p.write_json_to_file(json_elems_in_coll, alias, 'Elems_in_Collection_{}'.format(starting_pointer))

        """ Careful method of getting each object contentdm says is in a collection"""
        pointers_filetypes = [(single_record.find('dmrecord').text,
                               single_record.find('filetype').text,
                               ) for single_record in elems_in_coll_tree.findall('.//record')]

        for pointer, filetype in pointers_filetypes:
            if not pointer:  # skips file if a derivative -- only gets original versions
                continue

            if filetype != 'cpd':

                if '{}.json'.format(pointer) not in os.listdir('{}/Cached_Cdm_files/{}'.format(os.getcwd(), alias)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, alias, pointer)


                if '{}.xml'.format(pointer) not in os.listdir('{}/Cached_Cdm_files/{}'.format(os.getcwd(), alias)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, alias, pointer)

                item_xml_file = '{}/Cached_Cdm_files/{}/{}.xml'.format(os.getcwd(), alias, pointer)
                item_etree = etree.parse(item_xml_file)
                if item_etree.find('find') is not None:  # "find" is contentdm's abbr for 'contentdm file name'
                    pass
                    # binary = p.retrieve_binaries(alias, pointer, "_")
                    # p.write_binary_to_file(binary, alias, pointer, filetype)

            elif filetype == 'cpd':
                os.makedirs('Cached_Cdm_files/{}/Cpd'.format(alias), exist_ok=True)

                if '{}.json'.format(pointer) not in os.listdir('{}/Cached_Cdm_files/{}/Cpd'.format(os.getcwd(), alias)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, '{}/Cpd'.format(alias), pointer)

                if '{}.xml'.format(pointer) not in os.listdir('{}/Cached_Cdm_files/{}/Cpd'.format(os.getcwd(), alias)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), pointer)

                item_xml_file = '{}/Cached_Cdm_files/{}/Cpd/{}.xml'.format(os.getcwd(), alias, pointer)
                item_etree = etree.parse(item_xml_file)

                if '{}_cpd.xml'.format(pointer) not in os.listdir('{}/Cached_Cdm_files/{}/Cpd'.format(os.getcwd(), alias)):
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
                os.makedirs('Cached_Cdm_files/{}/Cpd/{}'.format(alias, cpd_pointer), exist_ok=True)
                for elem in subpointer_list:
                    if alias == 'LSU_SCE' and elem.text in ('269', '308', '258', '261'):
                        continue    # skipping known bad object
                    if "{}.xml".format(elem.text) not in os.listdir(os.path.join(alias_dir, 'Cpd', cpd_pointer)):
                        print(elem.text, 'xml not in folder')
                        p.write_xml_to_file(p.retrieve_item_metadata(alias, elem.text, 'xml'), alias, 'Cpd/{}/{}'.format(cpd_pointer, elem.text))
                    if "{}.json".format(elem.text) not in os.listdir(os.path.join(alias_dir, 'Cpd', cpd_pointer)):
                        print(elem.text, 'json not in folder')
                        p.write_json_to_file(p.retrieve_item_metadata(alias, elem.text, 'json'), alias, 'Cpd/{}/{}'.format(cpd_pointer, elem.text))

if __name__ == '__main__':
    """ Call just one collection, retrieve all metadata """
    # just_so_i_can_call_it('LSU_LNP')

    """ Call all collections, retrieve all metadata """

    coll_list_txt = p.retrieve_collections_list()
    p.write_xml_to_file(coll_list_txt, '.', 'Collections_List')
    coll_list_xml = etree.fromstring(bytes(bytearray(coll_list_txt, encoding='utf-8')))
    for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
        print(alias)
        just_so_i_can_call_it(alias)
