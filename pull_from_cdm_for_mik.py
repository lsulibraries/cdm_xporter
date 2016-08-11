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


def retrieve_collection_fields_xml(collection_alias):
    url = '{}dmGetCollectionFieldInfo/{}/xml'.format(url_prefix, collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_fields_json(collection_alias):
    url = '{}dmGetCollectionFieldInfo/{}/json'.format(url_prefix, collection_alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_elems_xml(collection_alias, fields_list, starting_pointer):
    url = '{}dmQuery/{}/0/{}/nosort/100/dmcreated!dmrecord/1/0/0/0/0/0/xml'.format(url_prefix, collection_alias, starting_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_elems_json(collection_alias, fields_list, starting_pointer):
    url = '{}dmQuery/{}/0/{}/nosort/100/dmcreated!dmrecord/1/0/0/0/0/0/json'.format(url_prefix, collection_alias, starting_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_item_metadata(collection_alias, item_pointer, form):
    url = '{}dmGetItemInfo/{}/{}/{}'.format(url_prefix, collection_alias, item_pointer, form)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_binaries(collection_alias, item_pointer, filetype):
    url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection/{}/id/{}/filename/unused.{}'.format(
        collection_alias, item_pointer, filetype)
    with urllib.request.urlopen(url) as response:
        return response.read()


def retrieve_compound_object(collection_alias, item_pointer):
    url = '{}dmGetCompoundObjectInfo/{}/{}/xml'.format(url_prefix, collection_alias, item_pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_parent_info(collection_alias, item_pointer, filetype):
    url = '{}GetParent/{}/{}/{}'.format(url_prefix, collection_alias, item_pointer, filetype)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def write_binary_to_file(binary, alias, new_filename, filetype):
    os.makedirs('../Cached_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../Cached_Cdm_files/{}/{}.{}'.format(alias, new_filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)


def write_xml_to_file(xml_text, alias, new_filename):
    os.makedirs('../Cached_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../Cached_Cdm_files/{}/{}.xml'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(xml_text)


def write_json_to_file(json_text, alias, new_filename):
    os.makedirs('../Cached_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../Cached_Cdm_files/{}/{}.json'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(json_text)


def write_admin_binary_to_file(binary, alias, new_filename, filetype):
    os.makedirs('../AdminPanel_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../AdminPanel_Cdm_files/{}/{}.{}'.format(alias, new_filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)


def write_admin_xml_to_file(xml_text, alias, new_filename):
    os.makedirs('AdminPanel_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../AdminPanel_Cdm_files/{}/{}.xml'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(xml_text)


def write_admin_json_to_file(json_text, alias, new_filename):
    os.makedirs('AdminPanel_Cdm_files/{}'.format(alias), exist_ok=True)
    filename = '../AdminPanel_Cdm_files/{}/{}.json'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(json_text)
