#! /usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET
import os


def export_pointers_from_contentdm(alias):
    query_url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmQuery/{}/0/covera/nosort/1024/1/0/0/0/0/0/0/xml'.format(alias)
    with urllib.request.urlopen(query_url) as response:
        return ET.fromstring(response.read())

def find_pointers(pointers_etree):
    return [pointer.findtext('.') for pointer in pointers_etree.findall('.//pointer')]

def retrieve_metadata(alias, pointer):
    meta_url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(alias, pointer)
    with urllib.request.urlopen(meta_url) as response:
        return response.read().decode(encoding='utf-8')

def retrieve_binaries_and_rename(alias, pointer, new_filename, filetype):
    file_url = 'https://cdm16313.contentdm.oclc.org/utils/getfile/collection/{}/id/{}/filename/{}.{}'.format(alias, pointer, new_filename, filetype)
    with urllib.request.urlopen(file_url) as response:
        return response.read()

def write_binary_to_file(binary, filename, filetype):
    if 'cdm_binaries' not in os.listdir(os.getcwd()):
        os.mkdir('cdm_binaries')
    filename = 'cdm_binaries/{}.{}'.format(filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)

def write_xml_to_file(xml_text, alias, pointer):
    if 'cdm_metadata_text' not in os.listdir(os.getcwd()):
        os.mkdir('cdm_metadata_text')
    filename = 'cdm_metadata_text/{}_{}.xml'.format(alias, pointer)
    with open(filename, 'w') as f:
        f.write(xml_text)

'''
collections
- collection
  - items
    - {compound obj
        - obj_meta}...
            - simple obj
                - meta
                - file
'''

if __name__ == '__main__':
    alias = 'p16313coll54'
    pointer = '64'
    temp_binary = retrieve_binaries_and_rename(alias, pointer, 'you_can_rename', 'jp2')
    write_binary_to_file(temp_binary, 'other_filename', 'jp2')
    # pointers_etree = export_pointers_from_contentdm(alias)
    # for pointer in find_pointers(pointers_etree):
    #     metadata_xml = retrieve_metadata(alias, pointer)
    #     write_to_file(metadata_xml, alias, pointer)
