#! /usr/bin/env python3

import os
import sys
import pull_from_cdm as p
import xml.etree.ElementTree as ET


def list_all_aliases():
    coll_list_xml = ET.fromstring(p.retrieve_collections_list())
    return [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]


def xmlify_a_collection(alias):
    if os.path.isfile("cdm_metadata_text/{}.xml".format(alias)):
        return
    collection_etree = ET.Element('collection', attrib={'alias': alias})
    elems_in_coll_xml = p.retrieve_elems_in_collection(alias, ['source', 'dmrecord', 'dmimage', 'find'])
    elems_in_coll_etree = ET.fromstring(elems_in_coll_xml)

    pointers_filetypes_sources = [(single_record.find('pointer').text,
                                   single_record.find('filetype').text,
                                   single_record.find('source').text)
                                  for single_record in elems_in_coll_etree.findall('.//record')
                                  ]
    for pointer, filetype, source in pointers_filetypes_sources:
        if filetype == 'cpd':
            print(alias, pointer)
            local_etree = ET.fromstring(p.retrieve_item_metadata(alias, pointer))
            local_etree = clean_up_compound_tags(alias, pointer, local_etree)
            local_etree.append(xmlify_a_compound(alias, pointer))
            collection_etree.append(local_etree)
        else:
            local_etree = xmlify_an_item(alias, pointer, filetype)
            collection_etree.append(local_etree)
    p.write_xml_to_file(ET.tostring(collection_etree, encoding="unicode", method="xml"), alias)


def xmlify_a_compound(alias, pointer):
    xml_text = p.retrieve_compound_object(alias, pointer)
    local_etree = ET.fromstring(xml_text)
    local_etree = clean_up_tags(alias, pointer, local_etree)
    for page_elem in local_etree.findall('.//page'):
        filename = page_elem.find('./pagefile').text
        local_pointer = page_elem.find('./pageptr').text
        name, filetype = os.path.splitext(filename)
        filetype = filetype.replace('.', '')
        if filetype == 'cpd':
            print('Script not built for nested compounds')
        else:
            print(alias, name, filetype)
            item_etree = xmlify_an_item(alias, local_pointer, filetype)
            local_etree.append(item_etree)
            # optional pull binary off content dm website
            # if not os.path.isfile("cdm_binaries/{}_{}.{}".format(alias, local_pointer, filetype)):
            #     p.write_binary_to_file(p.retrieve_binaries(alias, local_pointer, filetype), '{}_{}'.format(alias, local_pointer), filetype)
    return local_etree


def xmlify_an_item(alias, pointer, filetype):
    xml_text = p.retrieve_item_metadata(alias, pointer)
    local_etree = ET.fromstring(xml_text)
    local_etree = clean_up_tags(alias, pointer, local_etree)
    # This writes an xml file for each item.
    # p.write_xml_to_file(xml_text, '{}_{}'.format(alias, pointer))
    if not os.path.isfile("cdm_binaries/{}_{}.{}".format(alias, pointer, filetype)):
        pass
        # This write the binary to file
        # p.write_binary_to_file(p.retrieve_binaries(alias, pointer, filetype), '{}_{}'.format(alias, pointer), filetype)
    return local_etree


def lookup_coll_nicknames(alias):
    collection_fields = p.retrieve_collection_fields(alias)
    collection_fields_tree = ET.fromstring(collection_fields)
    nickname_dict = p.make_nickname_dict(collection_fields_tree)
    return nickname_dict


def clean_up_compound_tags(alias, pointer, xml_etree):
    for xml_tag in xml_etree.iter('xml'):
        xml_tag.tag = 'compound_object'
        xml_tag.set('pointer', pointer)
        xml_tag.set('alias', alias)
    for k, v in lookup_coll_nicknames(alias).items():
        for xml_tag in xml_etree.iter(k):
            xml_tag.tag = v
    return xml_etree


def clean_up_tags(alias, pointer, xml_etree):
    for xml_tag in xml_etree.iter('xml'):
        xml_tag.tag = 'simple_object'
        xml_tag.set('pointer', pointer)
        xml_tag.set('alias', alias)
    for xml_tag in xml_etree.iter('cpd'):
        xml_tag.tag = 'compound_object_wrapper'
    for k, v in lookup_coll_nicknames(alias).items():
        for xml_tag in xml_etree.iter(k):
            xml_tag.tag = v
    return xml_etree


if __name__ == '__main__':
    # alias = 'p16313coll81'
    # try:
    #     xmlify_a_collection(alias)
    # except OSError:
    #     print("Error:", sys.exc_info()[0].with_traceback())

    for alias in list_all_aliases():
        try:
            xmlify_a_collection(alias)
        except OSError:
            print("Error:", sys.exc_info()[0])
