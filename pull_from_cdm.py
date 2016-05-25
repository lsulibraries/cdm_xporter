#! /usr/bin/env python3

import urllib.request
import os


url_prefix = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q='


def retrieve_collections_list():
    url = '{}dmGetCollectionList/xml'.format(url_prefix)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_metadata(collection_alias):
    url = '{}dmGetCollectionArchivalInfo/{}/xml'.format(url_prefix, collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_total_recs(collection_alias):
    url = '{}dmQueryTotalRecs/{}|0/xml'.format(url_prefix, collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_fields(collection_alias):
    url = '{}dmGetCollectionFieldInfo/{}/xml'.format(url_prefix, collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_elems_in_collection(collection_alias, fields_list, starting_pointer):
    url = '{}dmQuery/{}/0/{}/nosort/1024/{}/0/0/0/0/xml'.format(url_prefix, collection_alias, '!'.join(fields_list), starting_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_item_metadata(collection_alias, item_pointer):
    url = '{}dmGetItemInfo/{}/{}/xml'.format(url_prefix, collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_binaries(collection_alias, item_pointer, filetype):
    url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection/{}/id/{}/filename/arbitrary.{}'.format(
        collection_alias, item_pointer, filetype
        )
    with urllib.request.urlopen(url) as response:
        return response.read()


def retrieve_compound_object(collection_alias, item_pointer):
    url = '{}dmGetCompoundObjectInfo/{}/{}/xml'.format(url_prefix, collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def write_binary_to_file(binary, alias, new_filename, filetype):
    os.makedirs('Collections/{}'.format(alias), exist_ok=True)
    filename = 'Collections/{}/{}.{}'.format(alias, new_filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)


def write_xml_to_file(xml_text, alias, new_filename):
    os.makedirs('Collections/{}'.format(alias), exist_ok=True)
    filename = 'Collections/{}/{}.xml'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(xml_text)
