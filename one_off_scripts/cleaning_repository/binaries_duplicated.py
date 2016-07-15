#! /usr/bin/env python3

import os


dupes = []
for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files/'):
    len_name = dict()
    for file in files:
        if ('xml' in file) or ('json' in file):
            continue
        file_size = os.path.getsize(os.path.join(root, file))
        if file_size == 0:
            continue
        if file_size in len_name:
            dupes.append((root, file, len_name[file_size], file_size))
        else:
            len_name[file_size] = file

print(len(dupes))


sames = []
for root, file_a, file_b, _ in dupes:
    with open(os.path.join(root, file_a), 'rb') as f:
        with open(os.path.join(root, file_b), 'rb') as g:
            if f.read() == g.read():
                sames.append((root, file_a, file_b))

print(sames)
