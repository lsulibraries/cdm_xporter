#! /usr/bin/env python3

import xmlify
import pull_from_cdm as p
# import pull_from_hd as p
import xml.etree.ElementTree as ET


p.write_xml_to_file(p.retrieve_collections_list(), '.', 'Collections_List')
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
alias = 'LSU_GFM'
# alias = 'p16313coll20'
# alias = 'LSU_MRF'


p.write_xml_to_file(p.retrieve_collection_metadata(alias), alias, 'Collection_Metadata')

collection_fields = p.retrieve_collection_fields(alias)
p.write_xml_to_file(collection_fields, alias, 'Collection_Fields')

collection_fields_etree = ET.fromstring(collection_fields)
# nickname_dict = p.make_nickname_dict(collection_fields_etree)

fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
xml_elems_in_coll = p.retrieve_elems_in_collection(alias, fields_to_retrieve)
p.write_xml_to_file(xml_elems_in_coll, alias, 'Elems_in_Collection')

elems_in_coll_tree = ET.fromstring(xml_elems_in_coll)

pointers_list = [item_pointer.findtext('.') for item_pointer in elems_in_coll_tree.findall('.//pointer')]

pointers_filetypes = [(single_record.find('dmrecord').text,
                       single_record.find('filetype').text,
                       ) for single_record in elems_in_coll_tree.findall('.//record')
                      ]

for pointer, filetype in pointers_filetypes:
    item_metadata = p.retrieve_item_metadata(alias, pointer)
    local_etree = ET.fromstring(item_metadata)
    local_etree = xmlify.add_tag_attributes(local_etree, local_etree)
    local_etree = xmlify.clean_up_tags(alias, pointer, local_etree, collection_fields_etree)
    p.write_xml_to_file(ET.tostring(local_etree, encoding="unicode", method="xml"), alias, pointer)

    if ET.fromstring(item_metadata).find('object'):  # "find" is contentdm's abbr for 'contentdm file name'
        binary = p.retrieve_binaries(alias, pointer, "something")
        p.write_binary_to_file(binary, alias, pointer, filetype)

    p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), alias, pointer, filetype)
