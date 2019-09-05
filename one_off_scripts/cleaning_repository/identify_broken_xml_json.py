#! /usr/bin/env python3

import os
import lxml.etree as etree
import json
import sys


def check(folder):
    cant_read = []
    cant_parse = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file[-4:] == '.xml':
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            file_etree = etree.parse(f)
                        except:
                            cant_parse.append(os.path.join(root, file))
                            print('cant parse', root, file)
                            continue
                        try:
                            file_etree.getroot()
                        except:
                            cant_parse.append(os.path.join(root, file))
                            print('cant interpret', root, file)
                            continue
                except:
                    cant_read.append(os.path.join(root, file))
                    print('cant read', root, file)
                    continue
            if file[-5:] == '.json':
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            json.load(f)
                        except:
                            cant_parse.append(os.path.join(root, file))
                            print('cant parse', root, file)
                            continue
                except:
                    cant_read.append(os.path.join(root, file))
                    print('cant read', root, file)
                    continue

    print('cant read:', cant_read)
    print('cant parse', cant_parse)


if __name__ == '__main__':
    try:
        folder = sys.argv[1]
    except IndexError:
        print('\nChange to: "python identify_broken_xml_json.py $folder\n\n')
        quit()
    check(folder)
