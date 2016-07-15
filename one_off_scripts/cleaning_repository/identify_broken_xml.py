#! /usr/bin/env python3

import os
import lxml.etree as etree
import json

cant_read = []
cant_parse = []

for root, dirs, files in os.walk('/media/garrett_armstrong/Data/Cached_Cdm_files'):
    for file in files:
        print(file)
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
print('\n\n')
print('cant parse', cant_parse)
