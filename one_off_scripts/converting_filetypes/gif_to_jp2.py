#! /usr/bin/env python3

import os
import subprocess
from time import sleep

for root, dirs, files in os.walk('/media/james/U/Cached_Cdm_files/PSL'):
    for file in files:
        if ('.gif' in file) and ('{}.jp2'.format(file.strip('.gif')) not in files) and (os.path.getsize("{}/{}".format(root, file)) > 0):
            print("convert {0}/{1} {0}/{2}.jp2".format(root, file, file.strip('.gif')))
            subprocess.run(["convert", "{}/{}".format(root, file), "{}/{}.jp2".format(root, file.strip('.gif'))], check=True)
            sleep(0.2)
