#! /usr/bin/env/ python3

import os

acceptable_filetypes = {'mp3', 'pdf', 'mp4', 'jp2'}

coll_filetypes = dict()
for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files/'):
    if ('p16313coll44' in root): # this collection is purely odd filetypes
        continue
    for file in files:

        if file.endswith('xml') or file.endswith('json'):
            continue
        if file.split('.')[-1] in acceptable_filetypes:
            continue
        if ('{}.mp3'.format(file.split('.')[0] in files)) or \
           ('{}.mp4'.format(file.split('.')[0] in files)) or \
           ('{}.pdf'.format(file.split('.')[0] in files)) or \
           ('{}.jp2'.format(file.split('.')[0] in files)):
            continue

        if root not in coll_filetypes:
            coll_filetypes[root] = {file, }
        else:
            coll_filetypes[root].add(file)

print(coll_filetypes)
