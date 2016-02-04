#! /usr/bin/env python3

import pull_from_cdm as p
import xml.etree.ElementTree as ET

alias = 'p16313coll54'  # Mingo Family ...

# p.write_xml_to_file(p.retrieve_collections_list(), 'Collections', 'List')
p.write_xml_to_file(p.retrieve_collection_metadata(alias), alias, 'Collection_Metadata')
p.write_xml_to_file(p.retrieve_collection_fields(alias), alias, 'Collection_Fields')

fields_to_retrieve = ['source', 'dmrecord', 'title', 'find']

xml_elems_in_coll = p.retrieve_elems_in_collection(alias, fields_to_retrieve)
p.write_xml_to_file(xml_elems_in_coll, alias, 'Elems_in_Collection')

elems_in_coll_tree = ET.fromstring(xml_elems_in_coll)

pointers_list = [item_pointer.findtext('.') for item_pointer in elems_in_coll_tree.findall('.//pointer')]
print(pointers_list)

for pointer in pointers_list:
    p.write_xml_to_file(p.retrieve_item_metadata(alias, pointer), alias, pointer)
    p.write_binary_to_file(p.retrieve_binaries(alias, pointer, 'jp2'), alias, pointer, 'jp2')
