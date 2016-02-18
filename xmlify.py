#! /usr/bin/env python3

import os
import pull_from_cdm as p
import xml.etree.ElementTree as ET


def xmlify_a_collection(alias):
    collection_etree = ET.Element(alias)
    elems_in_coll_xml = p.retrieve_elems_in_collection(alias, ['source', 'dmrecord', 'dmimage', 'find'])
    elems_in_coll_etree = ET.fromstring(elems_in_coll_xml)

    pointers_filetypes_sources = [(single_record.find('pointer').text,
                                   single_record.find('filetype').text,
                                   single_record.find('source').text)
                                  for single_record in elems_in_coll_etree.findall('.//record')
                                  ]
    for pointer, filetype, source in pointers_filetypes_sources:
        if filetype == 'cpd':
            local_etree = ET.fromstring(p.retrieve_item_metadata(alias, pointer))
            local_etree.append(xmlify_a_compound(alias, pointer))
            collection_etree.append(local_etree)
        else:
            local_etree = xmlify_an_item(alias, pointer, filetype)
            collection_etree.append(local_etree)
    p.write_xml_to_file(ET.tostring(collection_etree, encoding="unicode", method="xml"), alias)


def xmlify_a_compound(alias, pointer):
    meta_text = p.retrieve_compound_object(alias, pointer)
    local_etree = ET.fromstring(meta_text)
    for page_elem in local_etree.findall('.//page'):
        filename = page_elem.find('./pagefile').text
        local_pointer = page_elem.find('./pageptr').text
        name, filetype = os.path.splitext(filename)
        filetype = filetype.replace('.', '')
        if filetype == 'cpd':
            print('nested compounds!!!!!!!!!!!!!!!!!!!!!!!  Script not built for This!!!!!!!')
        else:
            print(alias, name, filetype)
            item_etree = xmlify_an_item(alias, local_pointer, filetype)
            local_etree.append(item_etree)
            # local_etree.append(ET.fromstring(p.retrieve_item_metadata(alias, local_pointer)))
            # # pass  # optional pull binary off content dm website
            # if not os.path.isfile("cdm_binaries/{}_{}.{}".format(alias, local_pointer, filetype)):
            #     p.write_binary_to_file(p.retrieve_binaries(alias, local_pointer, filetype), '{}_{}'.format(alias, local_pointer), filetype)
    return local_etree


def xmlify_an_item(alias, pointer, filetype):
    xml_text = p.retrieve_item_metadata(alias, pointer)
    xml_text = clean_up_metadata(alias, pointer, xml_text)
    # p.write_xml_to_file(xml_text, '{}_{}'.format(alias, pointer))
    if not os.path.isfile("cdm_binaries/{}_{}.{}".format(alias, pointer, filetype)):
        p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), '{}_{}'.format(alias, pointer), filetype)
    return ET.fromstring(xml_text)


def lookup_coll_nicknames(alias):
    collection_fields = p.retrieve_collection_fields(alias)
    collection_fields_tree = ET.fromstring(collection_fields)
    nickname_dict = p.make_nickname_dict(collection_fields_tree)
    return nickname_dict


def clean_up_metadata(alias, pointer, xml_text):
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
