#! /usr/bin/env python3

import lxml.etree as ET

with open('/media/garrett_armstrong/Storage/lsu_git/cdm_xporter/Collections/Collections_List.xml', 'r') as f:
    f_read = bytes(bytearray(f.read(), encoding='utf-8'))
    f_etree = ET.fromstring(f_read)

coll_list = []

for coll in f_etree.xpath('.//collection'):
    for item in coll.iterchildren():
        if item.tag == 'alias':
            alias = item.text.replace('/', '').strip()
        if item.tag == 'name':
            name = item.text.strip()
    coll_list.append('{}:  {}'.format(alias, name))


coll_list.sort()

for i in coll_list:
    print(i)
