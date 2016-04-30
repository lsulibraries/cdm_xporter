#! /usr/bin/env python3

import os
import lxml.etree as ET


def make_alias_terms_set():
    dict_a = dict()
    path = os.path.join(os.pardir, 'Collections')

    for entry in os.scandir(path):
        if entry.is_dir():
            alias = os.path.split(entry.path)[-1]
            etree = ET.parse(os.path.join(path, entry.path, 'Collection_Fields.xml'))
            alias_name_set = set()
            for name in etree.iterfind('.//name'):
                alias_name_set.add(name.text)
            dict_a[alias] = alias_name_set
    return dict_a
