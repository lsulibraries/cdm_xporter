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
        if filename == 'cpd':
            compound_root = ET.Element('{}_{}'.format(alias, pointer))
            # call depth_first search down folders()
                # add to etree as simple object if filetype != 'cpd'
                # add the folder level metadata as a layer on etree, then search each containing item
                    # add to etree if containing item filetype != 'cpd'
                    # else recurse above "folder level metadata as layer, then search each..." funct.
            pass
        else:
            item_etree = xmlify_an_object(alias, pointer)
            collection_etree.append(item_etree)

    p.write_xml_to_file(ET.tostring(collection_etree, encoding="unicode", method="xml"), alias)



def xmlify_an_object(alias, pointer):
    # modify to accept alias, pointer, & subpointer for compound collections
    xml_text = p.retrieve_item_metadata(alias, pointer)
    xml_text = clean_up_metadata(xml_text)
    # p.write_xml_to_file(xml_text, '{}_{}'.format(alias, pointer))
    # p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), '{}_{}'.format(alias, pointer), filetype)
    return ET.fromstring(item_metadata)

def xmlify_a_compound(alias, pointer):
    compound_meta = p.retrieve_compound_object(alias, pointer)

def clean_up_metadata(xml_text):
    for key, value in lookup_coll_nicknames(alias).items():
        value = value.replace(' ', '_').lower()
        xml_text = xml_text.replace('<{}>'.format(key), '<{}>'.format(value))
        xml_text = xml_text.replace('</{}>'.format(key), '</{}>'.format(value))
        xml_text = xml_text.replace('<{}/>'.format(key), '<{}/>'.format(value))
        xml_text = xml_text.replace('<{}>'.format('xml'), '<{}_{}>'.format(alias, pointer))
        xml_text = xml_text.replace('</{}>'.format('xml'), '</{}_{}>'.format(alias, pointer))
        xml_text = xml_text.replace('<{}/>'.format('xml'), '<{}_{}/>'.format(alias, pointer))
    xml_text = xml_text.replace('&#x27;', '&apos;')    
    return xml_text

