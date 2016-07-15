#! /usr/bin/env python3

import os
import subprocess
from time import sleep

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files'):
    for file in files:
        file_base, file_ext = file.split('.')
        for movie_type in ('m4v', 'mov', 'tif', 'png',):
            if (movie_type == file_ext.lower()) and ('{}.mp4'.format(file_base) not in files) and ('{}.mp3'.format(file_base) not in files) and (os.path.getsize("{}/{}".format(root, file)) > 0):
                print("convert {0}/{1} {0}/{2}.mp4".format(root, file, file_base))
                subprocess.run(["ffmpeg", "-i", "{}/{}".format(root, file), "{}/{}.mp4".format(root, file_base)], check=True)
                sleep(0.2)
