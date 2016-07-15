#! /usr/bin/env python3

import os


for root, dirs, files in os.walk('/media/james/U/Cached_Cdm_files'):
    current_dir_dict = dict()
    for file in files:
        filesize = os.path.getsize(os.path.join(root, file))
        if filesize not in current_dir_dict:
            current_dir_dict[str(os.path.getsize(os.path.join(root, file)))] = (root, file)
        else:
            print(root, file, current_dir_dict[filesize])
