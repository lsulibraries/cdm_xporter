#! /usr/bin/env/ python3

import os

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files'):
    for file in files:
        if ".ram.mp3" in file:
            print(file, file.replace('.ram.mp3', '.mp3'))
            os.rename(os.path.join(root, file), os.path.join(root, file.replace('.ram.mp3', '.mp3')))
        if ".rm.mp3" in file:
            print(file, file.replace('.rm.mp3', '.mp3'))
            os.rename(os.path.join(root, file), os.path.join(root, file.replace('.rm.mp3', '.mp3')))