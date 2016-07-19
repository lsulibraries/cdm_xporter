#!/usr/bin/env/ python3

import os

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files/'):
    for file in files:
        if ".mp4" in file:
            file_base, file_ext = file.split('.')
            if ('{}.png'.format(file_base) in files) or ('{}.tif'.format(file_base) in files):
                print(root, file)
                os.remove(os.path.join(root, file))
