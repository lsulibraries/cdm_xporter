#! /usr/bin/env python3

import urllib.request
import os

# "alias" is contentDM's term for collection name
# "pointer" is contentDM's term for item name


url_prefix = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q='


def retrieve_collections_list():
    url = '{}dmGetCollectionList/xml'.format(url_prefix)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_metadata(alias):
    url = '{}dmGetCollectionArchivalInfo/{}/xml'.format(url_prefix, alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_total_recs(alias):
    url = '{}dmQueryTotalRecs/{}|0/xml'.format(url_prefix, alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_fields_xml(alias):
    url = '{}dmGetCollectionFieldInfo/{}/xml'.format(url_prefix, alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_collection_fields_json(alias):
    url = '{}dmGetCollectionFieldInfo/{}/json'.format(url_prefix, alias)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_elems_in_collection(alias, starting_position, chunk_size, xml_or_json):
    fields = 'fullrs!find!dmaccess!dmimage!dmcreated!dmmodified!dmoclcno!dmrecord'
    url = '{}dmQuery/{}/0/{}/nosort/{}/{}/1/0/0/0/0/0/{}'.format(
        url_prefix, alias, fields, chunk_size, starting_position, xml_or_json)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_item_metadata(alias, pointer, xml_or_json):
    url = '{}dmGetItemInfo/{}/{}/{}'.format(url_prefix, alias, pointer, xml_or_json)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_compound_object(alias, pointer):
    url = '{}dmGetCompoundObjectInfo/{}/{}/xml'.format(url_prefix, alias, pointer)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_parent_info(alias, pointer, xml_or_json):
    url = '{}GetParent/{}/{}/{}'.format(url_prefix, alias, pointer, xml_or_json)
    with urllib.request.urlopen(url) as response:
        return response.read().decode(encoding='utf-8')


def retrieve_binary(alias, pointer):
    cdm_binary_url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection'
    url = '{}/{}/id/{}/filename/unused.unused'.format(cdm_binary_url, alias, pointer)
    with urllib.request.urlopen(url) as response:
        return response.read()


def write_xml_to_file(xml_text, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, '{}.xml'.format(filename))
    with open(filepath, 'w') as f:
        f.write(xml_text)


def write_json_to_file(json_text, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, '{}.json'.format(filename))
    with open(filepath, 'w') as f:
        f.write(json_text)


def write_binary_to_file(binary, folder, filename, filetype):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, '{}.{}'.format(filename, filetype))
    with open(filepath, 'bw') as f:
        f.write(binary)
