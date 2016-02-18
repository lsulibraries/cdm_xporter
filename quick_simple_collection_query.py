#! /usr/bin/env python3

import pull_from_cdm as p
import xml.etree.ElementTree as ET

p.write_xml_to_file(p.retrieve_collections_list(), '{}_{}'.format('Collections', 'List'))
# alias = 'p16313coll54'  # Mingo Family ...
# alias = 'p16313coll38'  # some collection with non-xml-compliant nicknames
alias = 'p120701coll15'  # some compound objects - some blocked from download
alias = 'p15140coll30'   # some compound objects

p.write_xml_to_file(p.retrieve_collection_metadata(alias), '{}_{}'.format(alias, 'Collection_Metadata'))

collection_fields = p.retrieve_collection_fields(alias)
p.write_xml_to_file(collection_fields, '{}_{}'.format(alias, 'Collection_Fields'))
collection_fields_tree = ET.fromstring(collection_fields)

nickname_dict = p.make_nickname_dict(collection_fields_tree)

fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
xml_elems_in_coll = p.retrieve_elems_in_collection(alias, fields_to_retrieve)
p.write_xml_to_file(xml_elems_in_coll, '{}_{}'.format(alias, 'Elems_in_Collection'))

elems_in_coll_tree = ET.fromstring(xml_elems_in_coll)

pointers_list = [item_pointer.findtext('.') for item_pointer in elems_in_coll_tree.findall('.//pointer')]

pointers_filetypes = [(single_record.find('dmrecord').text,
                       single_record.find('filetype').text,
                       ) for single_record in elems_in_coll_tree.findall('.//record')
                      ]

for pointer, filetype in pointers_filetypes:
    item_metadata = p.retrieve_item_metadata(alias, pointer)
    for key, value in nickname_dict.items():
        item_metadata = item_metadata.replace('<{}>'.format(key), '<{}>'.format(value.replace(' ', '_').lower()))
        item_metadata = item_metadata.replace('</{}>'.format(key), '</{}>'.format(value.replace(' ', '_').lower()))
        item_metadata = item_metadata.replace('<{}/>'.format(key), '<{}/>'.format(value.replace(' ', '_').lower()))

    p.write_xml_to_file(item_metadata, '{}_{}'.format(alias, pointer))

    # p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), '{}_{}'.format(alias, pointer), filetype)
