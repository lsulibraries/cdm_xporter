#! /usr/bin/env python3

import os

for root, dirs, files in os.walk('/media/garrett_armstrong/Data/Cached_Cdm_files'):
    for file in files:
        filepath = os.path.join(root, file)
        if os.path.getsize(filepath) == 0:
            print(filepath)
