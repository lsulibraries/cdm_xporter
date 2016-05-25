#! /usr/bin/env python3

import os
import lxml.etree as ET
import sys

sys.path.append("..")
from one_off_scripts.whats_the_extra_object import make_alias_list


def count_alias_objects_compounds(alias):
    count = 0
    compound = 0
    for filename in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        if 'Elems_in_Collection' in filename:
            with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, filename)) as f:
                f_read = bytes(bytearray(f.read(), encoding='utf-8'))
                f_etree = ET.fromstring(f_read)
            for elem in f_etree.xpath('.//record'):
                for subelem in elem.iter():
                    if subelem.tag == 'dmrecord':
                        if subelem.text:
                            count += 1
                    if subelem.tag == 'filetype':
                        if subelem.text in ('cpd'):
                            compound += 1
    return (alias, count, compound)

if __name__ == '__main__':
    for alias in make_alias_list():
        k = count_alias_objects_compounds(alias)
        if k[2] > 0:
            print(k)
