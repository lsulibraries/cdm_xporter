#! /usr/bin/env python3

import os
# import subprocess
# from time import sleep

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files/AAW'):
    for file in files:
        if (".sid" in file) and ("{}.jp2".format(file.strip('.sid')) not in files):
            print(root, file)
