#! /usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET
import os


def retrieve_collections_list():
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionList/xml'
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_collection_metadata(collection_alias):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionArchivalInfo/{}/xml'.format(collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_collection_fields(collection_alias):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionFieldInfo/{}/xml'.format(collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_elems_in_collection(collection_alias, fields_list):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmQuery/{}/0/{}/nosort/1024/1/0/0/0/0/0/0/xml'.format(collection_alias, '!'.join(fields_list))
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_item_metadata(collection_alias, item_pointer):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_binaries(collection_alias, item_pointer, filetype):
    url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection/{}/id/{}/filename/arbitrary.{}'.format(collection_alias, item_pointer, filetype)
    with urllib.request.urlopen(url) as response:
        return response.read()

def retrieve_compound_object(collection_alias, item_pointer):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCompoundObjectInfo/{}/{}/xml'.format(collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')

def write_binary_to_file(binary, collection_alias, item_pointer, filetype):
    if 'cdm_binaries' not in os.listdir(os.getcwd()):
        os.mkdir('cdm_binaries')
    filename = 'cdm_binaries/{}_{}.{}'.format(collection_alias, item_pointer, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)

def write_xml_to_file(xml_text, collection_alias, item_pointer):
    if 'cdm_metadata_text' not in os.listdir(os.getcwd()):
        os.mkdir('cdm_metadata_text')
    filename = 'cdm_metadata_text/{}_{}.xml'.format(collection_alias, item_pointer)
    with open(filename, 'w') as f:
        f.write(xml_text)


def find_item_pointers(item_pointers_etree):
    return [item_pointer.findtext('.') for item_pointer in item_pointers_etree.findall('.//pointer')]

'''
Collections
  Collection
    (("about this collection" paragraphs and info, not included in collection metadata))
    item
      item meta
      binary
    object (compound object)
      object meta
      item
        item meta?
        binary
        binary
        binary
'''

if __name__ == '__main__':
    pass

    #  Sample commands:
    #  write_xml_to_file(retrieve_collections_list(), 'Collections', 'List')
    #  write_xml_to_file(retrieve_collection_metadata(alias), alias, pointer)
    #  write_xml_to_file(retrieve_collection_fields(alias), alias, pointer)
    #  write_xml_to_file(retrieve_elems_in_collection(alias, ['dmrecord', 'fullrs', 'title', 'a', 'covera']), alias, pointer)
    #  write_xml_to_file(retrieve_item_metadata(alias, pointer), alias, pointer)
    #  write_binary_to_file(retrieve_binaries(alias, pointer, file_type), alias, pointer, file_type)












    # collection_alias = 'p16313coll54'
    # item_pointer = '64'
    # temp_binary = retrieve_binaries_and_rename(collection_alias, item_pointer, 'you_can_rename', 'jp2')
    # write_binary_to_file(temp_binary, 'other_filename', 'jp2')
    # item_pointers_etree_elem = export_item_pointers_from_contentdm(collection_alias)
    # for item_pointer in find_item_pointers(item_pointers_etree):
    #     metadata_xml = retrieve_item_metadata(collection_alias, item_pointer)
    #     write_to_file(metadata_xml, collection_alias, item_pointer)
