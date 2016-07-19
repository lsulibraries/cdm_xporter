#! /usr/bin/env python3

import os
import re

print(type(os.walk('/media/james/BlackToshiba/Cached_Cdm_files')))

simples_dict = dict()
compounds_dict = dict()
alias_smpl_cmpds = dict()
 
compiled_re = re.compile('[0-9]+.xml')

for root, dirs, files in os.walk('/media/james/BlackToshiba/Cached_Cdm_files'):
    root_pos = [i for i in root.split('/')].index('Cached_Cdm_files')
    if len(root.split('/')) == root_pos + 3:
        compounds_dict[root.split('/')[root_pos+1]] = dirs
        alias = root.split('/')[root_pos + 1]
        print(alias)

    elif len(root.split('/')) == root_pos + 2:
        pointer_xmls = [i.split('.')[0] for i in files if compiled_re.match(i)]
        simples_dict[root.split('/')[root_pos+1]] = pointer_xmls
        alias = root.split('/')[root_pos + 1]
        print(alias)

    else:
        continue

all_collections = set(i for i in simples_dict)
for i in compounds_dict:
    all_collections.add(i)


for alias in all_collections:
    if alias in simples_dict:
        simples_pointers = tuple(i for i in simples_dict[alias])
    else:
        simples_pointers = tuple()
    if alias in compounds_dict:
        compounds_pointers = tuple(i for i in compounds_dict[alias])
    else:
        compounds_pointers = tuple()
    alias_smpl_cmpds[alias] = (simples_pointers, compounds_pointers)


text_output = ''
for i in alias_smpl_cmpds:
    new_line = '{}\nSimples: {}\nCompounds: {}\n\n'.format(i, alias_smpl_cmpds[i][0], alias_smpl_cmpds[i][1])
    text_output = text_output + new_line


print(text_output)


with open('compound_simple_pointers.txt', 'w') as f:
    f.write(text_output)

