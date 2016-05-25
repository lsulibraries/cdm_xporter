#! /usr/bin/env python3

import os
from lxml import etree


os.chdir('..')

alias = 'p16313coll1'

for file in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
    for other_file in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        if file != other_file:
            if file[:-4].isnumeric() and other_file[:-4].isnumeric():
                with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, file), 'r') as f:
                    with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, other_file), 'r') as g:
                        f_read = bytes(bytearray(f.read(), encoding='utf-8'))
                        g_read = bytes(bytearray(g.read(), encoding='utf-8'))
                        f_etree, g_etree = etree.fromstring(f_read), etree.fromstring(g_read)
                        if f_etree.xpath('//xml/cdmfilesize')[0].text == g_etree.xpath('//xml/cdmfilesize')[0].text:
                            print(file, other_file)
