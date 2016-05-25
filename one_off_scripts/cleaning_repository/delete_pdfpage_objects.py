#! /usr/bin/python3

import os
import shutil

import lxml.etree as ET


pdfpage_objects = []
for root, dirs, files in os.walk('Cached_Cdm_files'):
    if 'Cpd' in root and dirs != []:
        if len(dirs) > 0:
            for file in files:
                if 'xml' in file:
                    etree = ET.parse(os.path.join(root, file))
                    i = etree.xpath("//pagefile")
                    if i:
                        if i[0].text and 'pdfpage' in i[0].text:
                            pdfpage_objects.append((root, file))

for i in pdfpage_objects:
    filepath = os.path.join(i[0], i[1].split('_')[0])
    if os.path.exists(filepath):
        print(filepath)
        shutil.rmtree(filepath)
