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
    fetch_meta_url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(alias, pointer)
    with urllib.request.urlopen(fetch_meta_url) as response:
        return response.read().decode(encoding='utf-8')

def write_to_file(xml_text, alias, pointer):
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
    pointers_etree = export_pointers_from_contentdm(alias)
    for pointer in find_pointers(pointers_etree):
        metadata_xml = retrieve_metadata(alias, pointer)
        write_to_file(metadata_xml, alias, pointer)
