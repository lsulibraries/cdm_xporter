#! /usr/bin/env python3

import pull_from_cdm as p
import xml.etree.ElementTree as ET


def lookup_coll_nicknames(alias):
    collection_fields = p.retrieve_collection_fields(alias)
    collection_fields_tree = ET.fromstring(collection_fields)
    nickname_dict = p.make_nickname_dict(collection_fields_tree)
    return nickname_dict


def xmlify_a_collection(alias):
    elems_in_coll_xml = p.retrieve_elems_in_collection(alias, ['source', 'dmrecord', 'dmimage', 'find'])
    elems_in_coll_etree = ET.fromstring(elems_in_coll_xml)

    pointers_filetypes = [(single_record.find('dmrecord').text,
                           single_record.find('filetype').text,
                           ) for single_record in elems_in_coll_etree.findall('.//record')
                          ]

    collection_etree = ET.Element(alias)
    for pointer, filetype in pointers_filetypes:
        object_xml = xmlify_an_object(alias, pointer)
        collection_etree.append(ET.fromstring(object_xml))

    p.write_xml_to_file(ET.tostring(collection_etree, encoding="unicode", method="xml"), alias)


def xmlify_an_object(alias, pointer):
    item_metadata = p.retrieve_item_metadata(alias, pointer)
    for key, value in lookup_coll_nicknames(alias).items():
        value = value.replace(' ', '_').lower()
        item_metadata = item_metadata.replace('<{}>'.format(key), '<{}>'.format(value))
        item_metadata = item_metadata.replace('</{}>'.format(key), '</{}>'.format(value))
        item_metadata = item_metadata.replace('<{}/>'.format(key), '<{}/>'.format(value))

        item_metadata = item_metadata.replace('<{}>'.format('xml'), '<{}_{}>'.format(alias, pointer))
        item_metadata = item_metadata.replace('</{}>'.format('xml'), '</{}_{}>'.format(alias, pointer))
        item_metadata = item_metadata.replace('<{}/>'.format('xml'), '</{}_{}/>'.format(alias, pointer))
    return item_metadata
