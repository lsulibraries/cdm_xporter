#! /usr/bin/env python3

import os
import xml.etree.ElementTree as ET


dict_a = dict()

file_dir = '/home/garrett_armstrong/lsu_libraries_git_projects/cdm_xporter/Collections/'


def make_alias_terms_set():
    for alias in os.listdir(file_dir):
        if alias not in ['Collections_List.xml']:
            for filename in os.listdir(file_dir + alias):
                if filename == 'Collection_Fields.xml':
                    with open(file_dir + '/' + alias + '/' + filename, 'r') as f:
                        print(alias, filename)
                        xmltext = f.read()
                        etree = ET.fromstring(xmltext)
                        alias_name_set = set()
                        for name in etree.iterfind('.//name'):
                            alias_name_set.add(name.text)
                        dict_a[alias] = alias_name_set
    return dict_a
