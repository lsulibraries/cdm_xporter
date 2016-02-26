#! /usr/bin/env python3

import urllib.request
import os
from xml.sax.saxutils import escape


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


def find_item_pointers(item_pointers_etree):
    return [item_pointer.findtext('.') for item_pointer in item_pointers_etree.findall('.//pointer')]


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
