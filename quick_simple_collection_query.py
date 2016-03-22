#! /usr/bin/env python3

import os
import xml.etree.ElementTree as ET
import urllib.request

import xmlify
import pull_from_cdm as p
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


def just_so_i_can_call_it(alias):
    if alias not in os.listdir('{}/Collections/'.format(os.getcwd())):
        os.mkdir(str('{}/Collections/{}').format(os.getcwd(), alias))

    if 'Collection_Metadata.xml' not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        p.write_xml_to_file(p.retrieve_collection_metadata(alias), alias, 'Collection_Metadata')

    if 'Collection_Fields.xml' not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        collection_fields = p.retrieve_collection_fields(alias)
        p.write_xml_to_file(collection_fields, alias, 'Collection_Fields')
    else:
        collection_fields = read_file('{}/Collections/{}/Collection_Fields.xml'.format(os.getcwd(), alias))
    collection_fields_etree = ET.fromstring(collection_fields)

    if 'Elems_in_Collection.xml' not in os.listdir('{}/Collections/{}/'.format(os.getcwd(), alias)):
        fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
        xml_elems_in_coll = p.retrieve_elems_in_collection(alias, fields_to_retrieve)
        p.write_xml_to_file(xml_elems_in_coll, alias, 'Elems_in_Collection')
    else:
        xml_elems_in_coll = read_file('{}/Collections/{}/Elems_in_Collection.xml'.format(os.getcwd(), alias))
    elems_in_coll_tree = ET.fromstring(xml_elems_in_coll)



    """ Careful method of getting each object contentdm says is in a collection"""
    pointers_filetypes = [(single_record.find('dmrecord').text,
                           single_record.find('filetype').text,
                           ) for single_record in elems_in_coll_tree.findall('.//record')]
    for pointer, filetype in pointers_filetypes:
        print(pointer, filetype, 'about to get')
        # if not pointer:  # skips file if binary not shared by collection owner
        #     continue
        if '{}.xml'.format(pointer) not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
            item_metadata = p.retrieve_item_metadata(alias, pointer)
            local_etree = ET.fromstring(item_metadata)
            # local_etree = xmlify.add_tag_attributes(local_etree, collection_fields_etree)
            #local_etree = xmlify.clean_up_tags(alias, pointer, local_etree, collection_fields_etree)
            p.write_xml_to_file(ET.tostring(local_etree, encoding="unicode", method="xml"), alias, pointer)

        # if ET.fromstring(item_metadata).find('object'):  # "find" is contentdm's abbr for 'contentdm file name'
        #     binary = p.retrieve_binaries(alias, pointer, "something")
        #     p.write_binary_to_file(binary, alias, pointer, filetype)

        # p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), alias, pointer, filetype)

    # """Brute force method of getting every possible object from a collection, even if contentdm doesn't say it's inside"""

    # blank_count = 0
    # for i in range(31000):
    #     if '{}.xml'.format(i) not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
    #         url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(alias, str(i))
    #         with urllib.request.urlopen(url) as response:
    #             html_text = response.read()
    #             if '<message>Requested item not found</message>' in html_text.decode('utf-8'):
    #                 print('found blank site', i)
    #                 blank_count += 1
    #             else:
    #                 item_metadata = p.retrieve_item_metadata(alias, i)
    #                 local_etree = ET.fromstring(item_metadata)
    #                 p.write_xml_to_file(ET.tostring(local_etree, encoding="unicode", method="xml"), alias, i)
    #                 print(alias, i)
    #                 blank_count = 0




def read_file(filename):
    with open(filename) as f:
        return f.read()

if __name__ == '__main__':
    """ Call just one collection, retrieve all metadata """
    # just_so_i_can_call_it('BRS')


    """ Call all collections, retrieve all metadata """
    coll_list_txt = p.retrieve_collections_list()
    p.write_xml_to_file(coll_list_txt, '.', 'Collections_List')
    coll_list_xml = ET.fromstring(coll_list_txt)
    for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
        print(alias)
        just_so_i_can_call_it(alias)
