#! /usr/bin/env python3

import os
from lxml import etree


os.chdir('..')

alias = 'BRS'

for hidden_file in os.listdir('{}/Collections/{}/HiddenPointers'.format(os.getcwd(), alias)):
    with open('{}/Collections/{}/HiddenPointers/{}'.format(os.getcwd(), alias, hidden_file), 'r') as f:
        f_read = f.read()
        f_read = bytes(bytearray(f_read, encoding='utf-8'))
        hidden_etree = etree.fromstring(f_read)
        for known_file in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
            if known_file != 'HiddenPointers':
                with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, known_file), 'r') as k:
                    k_read = k.read()
                    k_read = bytes(bytearray(k_read, encoding='utf-8'))
                    known_etree = etree.fromstring(k_read)
                    try:
                        if hidden_etree.xpath('//xml/title')[0].text == known_etree.xpath('//xml/title')[0].text:
                            print('same title in: {} {}'.format(hidden_file, known_file))
                    except IndexError:
                        print('one may not have a Title field: {}, {}'.format(hidden_file, known_file))
