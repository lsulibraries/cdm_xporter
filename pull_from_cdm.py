#! /usr/bin/env python3

import urllib.request
import os


def retrieve_collections_list():
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionList/xml'
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_metadata(collection_alias):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionArchivalInfo/{}/xml'.format(
        collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_fields(collection_alias):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCollectionFieldInfo/{}/xml'.format(
        collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_elems_in_collection(collection_alias, fields_list):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmQuery/{}/0/{}/nosort/1024/1/0/0/0/0/0/0/xml'.format(
        collection_alias, '!'.join(fields_list))
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_item_metadata(collection_alias, item_pointer):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(
        collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_binaries(collection_alias, item_pointer, filetype):
    url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection/{}/id/{}/filename/arbitrary.{}'.format(
        collection_alias, item_pointer, filetype)
    with urllib.request.urlopen(url) as response:
        return response.read()


def retrieve_compound_object(collection_alias, item_pointer):
    url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetCompoundObjectInfo/{}/{}/xml'.format(
        collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def write_binary_to_file(binary, alias, new_filename, filetype):
    make_directory_tree(alias)
    filename = 'Collections/{}/{}.{}'.format(alias, new_filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)


def write_xml_to_file(xml_text, alias, new_filename):
    make_directory_tree(alias)
    filename = 'Collections/{}/{}.xml'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(xml_text)


def make_directory_tree(alias):
    if 'Collections' not in os.listdir(os.getcwd()):
        os.mkdir('Collections')
    if alias not in os.listdir(os.getcwd() + '/Collections') and alias not in ('.', '..'):
        os.mkdir('Collections/{}'.format(alias))
