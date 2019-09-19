#! /usr/bin/env python3

import os


pointers = [
    os.path.splitext(file)[0]
    for file in os.listdir('/media/francis/Storage/LNP_Source_datas/CachedCdmFilesReady/LSU_LNP/')
    if os.path.splitext(file)[1] == '.pdf'
]
cpd_pointers = [
    os.path.splitext(file)[0].replace('_cpd', '')
    for file in os.listdir('/media/francis/Storage/LNP_Source_datas/CachedCdmFilesReady/LSU_LNP/Cpd/')
    if '_cpd.xml' in file
]


template = f"""{{"pager":{{"start": "1", "maxrecs": "100", "total": {len(pointers)+len(cpd_pointers)}}},"records": ["""
for pointer in pointers:
    template += f"""{{"collection": "LSU_LNP", "pointer": {pointer}, "filetype": "pdf", "parentobject": -1, "dmrecord": "{pointer}", "find": "{pointer}.pdf"}},"""
for pointer in cpd_pointers:
    template += f"""{{"collection": "LSU_LNP", "pointer": {pointer}, "filetype": "cpd", "parentobject": -1, "dmrecord": "{pointer}", "find": "{pointer}.cpd"}},"""
template = template[:-1]
template += "]}"
print(template)
