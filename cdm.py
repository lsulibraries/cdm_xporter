#! /usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET

'''

collections = ['p16313coll54']


collections
- collection
  - items
    - {compound obj
        - obj_meta}...
            - simple obj
                - meta
                - file

alias

field list
- map from nick to label
pointer list

item
'''
alias = 'p16313coll54'
query_url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmQuery/{}/0/covera/nosort/1024/1/0/0/0/0/0/0/xml'.format(alias)
# print(query_url)
with urllib.request.urlopen(query_url) as response:
   pointers_response_xml = ET.fromstring(response.read())

list_of_pointers = []
for pointer in pointers_response_xml.findall('.//pointer'):
    pointer_text = pointer.findtext('.')
    list_of_pointers.append(pointer_text)


for p in list_of_pointers:
    fetch_meta_url = 'https://server16313.contentdm.oclc.org/dmwebservices/index.php?q=dmGetItemInfo/{}/{}/xml'.format(alias, p)
    with urllib.request.urlopen(fetch_meta_url) as response:
        meta = response.read()
        filename = '{}_{}.xml'.format(alias, p)
        with open(filename, 'w') as f:
            f.write(meta.decode(encoding='UTF-8'))

# class FileAndMetadata (self):

#     def __init__(self, meta):
#         self.meta = meta

#     def get_file(self, pointer):
