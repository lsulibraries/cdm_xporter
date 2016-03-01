#! /usr/bin/env python3

import os
import sys
import pull_from_cdm as p
# import pull_from_hd as p
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


def list_all_aliases():
    coll_list_xml = ET.fromstring(p.retrieve_collections_list())
    return [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]


def grab_collection_fields(alias):
    collection_fields = p.retrieve_collection_fields(alias)
    return ET.fromstring(collection_fields)


def grab_elems_in_coll(alias):
    elems_in_coll_xml = p.retrieve_elems_in_collection(alias, ['source', 'dmrecord', 'dmimage', 'find'])
    return ET.fromstring(elems_in_coll_xml)


def xmlify_a_collection(alias):
    # if os.path.isfile("Collections/{}/Whole_Collection.xml".format(alias)):
        # return  # skip collection if an xml already computed & saved there.
    elems_in_coll_etree = grab_elems_in_coll(alias)
    collection_fields_etree = grab_collection_fields(alias)
    pointers_filetypes = [(single_record.find('pointer').text,
                           single_record.find('filetype').text,)
                          for single_record in elems_in_coll_etree.findall('.//record')
                          ]
    collection_etree = ET.Element('collection', attrib={'alias': alias})
    for pointer, filetype in pointers_filetypes:
        if filetype == 'cpd':
            local_etree = ET.fromstring(p.retrieve_item_metadata(alias, pointer))
            # following if clause catches weird case when binary is in root of compound object.
            if 'object' in [i.tag for i in local_etree.getchildren()]:
                bin_name, bin_ext = os.path.splitext(local_etree.find('object').text)
                bin_ext = bin_ext.strip('.')
                binary = p.retrieve_binaries(alias, pointer, bin_ext)
                p.write_binary_to_file(binary, alias, pointer, bin_ext)
            local_etree = clean_up_compound_tags(alias, pointer, local_etree, collection_fields_etree)
            local_etree.append(xmlify_a_compound(alias, pointer, collection_fields_etree))
            collection_etree.append(local_etree)
        else:
            local_etree = xmlify_an_item(alias, pointer, filetype, collection_fields_etree)
            collection_etree.append(local_etree)
    p.write_xml_to_file(ET.tostring(collection_etree, encoding="unicode", method="xml"), alias, "Whole_Collection")


def xmlify_a_compound(alias, pointer, collection_fields_etree):
    xml_text = p.retrieve_compound_object(alias, pointer)
    local_etree = ET.fromstring(xml_text)
    local_etree = add_tag_attributes(collection_fields_etree, local_etree)
    local_etree = clean_up_tags(alias, pointer, local_etree, collection_fields_etree)

    for page_elem in local_etree.findall('.//page'):
        filename = page_elem.find('./pagefile').text
        local_pointer = page_elem.find('./pageptr').text
        name, filetype = os.path.splitext(filename)
        filetype = filetype.replace('.', '')
        if filetype == 'cpd':
            print('Script not built for nested compounds')
        else:
            print(alias, name, filetype)
            item_etree = xmlify_an_item(alias, local_pointer, filetype, collection_fields_etree)
            local_etree.append(item_etree)
    return local_etree


def xmlify_an_item(alias, pointer, filetype, collection_fields_etree):
    xml_text = p.retrieve_item_metadata(alias, pointer)
    local_etree = ET.fromstring(xml_text)
    local_etree = add_tag_attributes(local_etree, collection_fields_etree)
    local_etree = clean_up_tags(alias, pointer, local_etree, collection_fields_etree)

    if not os.path.isfile("cdm_binaries/{}_{}.{}".format(alias, pointer, filetype)):
        pass
        # This write the binary on the simple object level to file
        binary = p.retrieve_binaries(alias, pointer, filetype)
        p.write_binary_to_file(binary, alias, pointer, filetype)
    return local_etree


def clean_up_compound_tags(alias, pointer, xml_etree, collection_fields_etree):
    for xml_tag in xml_etree.iter('xml'):
        xml_tag.tag = 'compound_object'
        xml_tag.set('pointer', pointer)
        xml_tag.set('alias', alias)
    for k, v in lookup_coll_nicknames(alias, collection_fields_etree).items():
        for xml_tag in xml_etree.iter(k):
            xml_tag.tag = v
    return xml_etree


def clean_up_tags(alias, pointer, xml_etree, collection_fields_etree):
    for xml_tag in xml_etree.iter('xml'):
        xml_tag.tag = 'simple_object'
        xml_tag.set('pointer', pointer)
        xml_tag.set('alias', alias)
    for xml_tag in xml_etree.iter('cpd'):
        xml_tag.tag = 'compound_object_wrapper'
    for k, v in lookup_coll_nicknames(alias, collection_fields_etree).items():
        for xml_tag in xml_etree.iter(k):
            xml_tag.tag = v
    return xml_etree


def lookup_coll_nicknames(alias, collection_fields_etree):
    nickname_dict = make_nickname_dict(collection_fields_etree)
    return nickname_dict


def make_nickname_dict(collection_fields_etree):
    nickname_dict = dict()
    for group in collection_fields_etree.findall('field'):
        nick, name = None, None
        for child in group.getchildren():
            if child.tag == 'name':
                name = child.text
                for invalid in ('/', '(', ')', ' ', "'", '"',):
                    name = name.replace(invalid, '_').lower()
            if child.tag == 'nick':
                nick = child.text
        if nick and name:
            nickname_dict[nick] = name
    return nickname_dict


def add_tag_attributes(xml_etree, collection_fields_etree):
    for tag in xml_etree.iter():
        fieldname_dict = make_fieldnames_dict(tag.tag, collection_fields_etree)
        if fieldname_dict:
            for k, v in fieldname_dict.items():
                tag.set(k, v)
    return xml_etree


def make_fieldnames_dict(nickname, collection_fields_etree):
    fieldnames_dict = dict()
    for field in collection_fields_etree.iter('field'):
        for elem in field.getchildren():
            if elem.text == nickname:
                for tag in field.findall('.//'):
                    if tag.tag and tag.text:
                        if tag.tag in {'dc', 'find', 'name', 'nick', 'size', 'type', 'vocab', 'req', 'search', 'vocab', 'vocdb', 'admin', 'readonly', }:
                            tag.text = escape(tag.text)
                            fieldnames_dict[tag.tag] = tag.text
    return fieldnames_dict


if __name__ == '__main__':
    alias = 'LSU_GFM'
    # try:
    xmlify_a_collection(alias)
    # except OSError:
    #     print("Error:", sys.exc_info()[0].with_traceback())

    # THIS RUNS THE WHOLE CONTENTDM
    # for alias in list_all_aliases():
    #     try:
    #         xmlify_a_collection(alias)
    #     except OSError:
    #         print("Error:", sys.exc_info()[0].with_traceback())
