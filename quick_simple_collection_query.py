#! /usr/bin/env python3

import os
import lxml.etree as etree
# import urllib.request

# import xmlify
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


def read_file(filename):
    with open(filename) as f:
        return f.read()


def just_so_i_can_call_it(alias):
    repo_dir = '{}/{}'.format(os.getcwd(), 'Collections')
    alias_dir = '{}/{}'.format(repo_dir, alias)

    if alias not in os.listdir(repo_dir):
        os.mkdir(str('{}/Collections/{}').format(os.getcwd(), alias))

    if 'Collection_Metadata.xml' not in os.listdir(alias_dir):
        p.write_xml_to_file(p.retrieve_collection_metadata(alias), alias, 'Collection_Metadata')

    if 'Collection_TotalRecs.xml' not in os.listdir(alias_dir):
        p.write_xml_to_file(p.retrieve_collection_total_recs(alias), alias, 'Collection_TotalRecs')

    if 'Collection_Fields.xml' not in os.listdir(alias_dir):
        collection_fields = p.retrieve_collection_fields(alias)
        p.write_xml_to_file(collection_fields, alias, 'Collection_Fields')
    else:
        collection_fields = read_file('{}/Collections/{}/Collection_Fields.xml'.format(os.getcwd(), alias))
    collection_fields_etree = etree.fromstring(bytes(bytearray(collection_fields, encoding='utf-8')))

    total_recs_etree = etree.fromstring(bytes(bytearray(p.retrieve_collection_total_recs(alias), encoding='utf-8')))
    num_of_pointers = int(total_recs_etree.xpath('.//total')[0].text)
    groups_of_1024 = (num_of_pointers // 1024) + 1

    for num in range(groups_of_1024):
        starting_pointer = (num * 1024) + 1                         # why the heavens does contentdm start counting at 1?
                                                                    # also, why can't cdm cound above 10000??
        if 'Elems_in_Collection_{}.xml'.format(starting_pointer) not in os.listdir('{}/Collections/{}/'.format(os.getcwd(), alias)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            xml_elems_in_coll = p.retrieve_elems_in_collection(alias, fields_to_retrieve, starting_pointer)
            p.write_xml_to_file(xml_elems_in_coll, alias, 'Elems_in_Collection_{}'.format(starting_pointer))

        else:
            xml_elems_in_coll = read_file('{}/Collections/{}/Elems_in_Collection_{}.xml'.format(os.getcwd(), alias, starting_pointer))
        elems_in_coll_tree = etree.fromstring(bytes(bytearray(xml_elems_in_coll, encoding='utf-8')))

        # """ Careful method of getting each object contentdm says is in a collection"""
        # pointers_filetypes = [(single_record.find('dmrecord').text,
        #                        single_record.find('filetype').text,
        #                        ) for single_record in elems_in_coll_tree.findall('.//record')]
        # for pointer, filetype in pointers_filetypes:
        #     if not pointer:  # skips file if a derivative -- only gets original versions
        #         print('{} {} not pointer, filetype'.format(pointer, filetype))

        #     elif '{}.xml'.format(pointer) not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        #         item_metadata = p.retrieve_item_metadata(alias, pointer)
        #         local_etree = etree.fromstring(bytes(bytearray(item_metadata, encoding='utf-8')))
        #         # local_etree = xmlify.add_tag_attributes(local_etree, collection_fields_etree)
        #         # local_etree = xmlify.clean_up_tags(alias, pointer, local_etree, collection_fields_etree)
        #         p.write_xml_to_file(etree.tostring(local_etree, encoding="unicode", method="xml"), alias, pointer)

            # if etree.fromstring(item_metadata).find('object'):  # "find" is contentdm's abbr for 'contentdm file name'
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
    #                 local_etree = etree.fromstring(item_metadata)
    #                 p.write_xml_to_file(etree.tostring(local_etree, encoding="unicode", method="xml"), alias, i)
    #                 print(alias, i)
    #                 blank_count = 0


if __name__ == '__main__':
    """ Call just one collection, retrieve all metadata """
    # just_so_i_can_call_it('BRS')

    """ Call all collections, retrieve all metadata """
    coll_list_txt = p.retrieve_collections_list()
    if 'Collections' not in os.listdir(os.getcwd()):
        os.mkdir('{}/Collections'.format(os.getcwd()))
    p.write_xml_to_file(coll_list_txt, '.', 'Collections_List')
    coll_list_xml = etree.fromstring(bytes(bytearray(coll_list_txt, encoding='utf-8')))
    for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
        print(alias)
        just_so_i_can_call_it(alias)
