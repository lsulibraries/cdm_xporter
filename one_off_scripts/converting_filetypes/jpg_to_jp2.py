#! /usr/bin/env python3

import os
import subprocess
from time import sleep

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files/LPS'):
    for file in files:
        if ('.jpg' in file) and ('{}.jp2'.format(file.strip('.jpg')) not in files) and (os.path.getsize("{}/{}".format(root, file)) > 0):
            print("convert {0}/{1} {0}/{2}.jp2".format(root, file, file.strip('.jpg')))
            subprocess.run(["convert", "{}/{}".format(root, file), "{}/{}.jp2".format(root, file.strip('.jpg'))], check=True)
            sleep(0.2)
