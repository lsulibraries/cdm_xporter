#! /usr/bin/env/ python3

import os
import lxml.etree as etree

file_formats = set()
broken_files = []

for root, dirs, files in os.walk('/media/garrett_armstrong/Data/Cached_Cdm_files'):
    if ('AWW' in root) or ('LPH' in root) or ('LSUHSC_NCC' in root) or \
    ('p15140coll28' in root) or ('LSU_JJA' in root) or ('p120701coll24' in root) or \
    ('p15140coll43' in root) or ('p16313coll51' in root) or ('Tensas' in root) or \
    ('p15140coll44' in root) or ('p15140coll1' in root) or ('SartainEngravings' in root) or \
    ('LSU_LHC' in root) or ('p16313coll65' in root) or ('p16313coll21' in root) or \
    ('NewOrleans' in root) or ('p15140coll61' in root) or ('p120701coll27' in root) or \
    ('p120701coll27' in root) or('UNO_ANI' in root):
        continue
    for file in files:
        if file.split('.')[0].isnumeric():
            orig_ext = file.split('.')[-1]
            if orig_ext in ('xml', ):
                file_etree = etree.parse(os.path.join(root, file))
                format_field = file_etree.xpath("./format")
                try:
                    file_formats.add(format_field[0].text)
                except:
                    pass
                try:
                    if file_etree.xpath("./message")[0].text == "Requested item not found":
                        broken_files.append(os.path.join(root, file))
                except:
                    pass
    print(root)
    print(file_formats)

print(file_formats)
print(broken_files)
