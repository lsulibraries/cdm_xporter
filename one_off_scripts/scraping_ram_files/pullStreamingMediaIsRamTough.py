# usr/bin/env python3

import os
import requests

ram_collections = ["RJR", "LSM_KOH", "JAZ", "LSU_SCE", "LOH"]

for alias in ram_collections:
    filepath = "../../Cached_Cdm_files/{}".format(alias)
    for directory, subdirectories, files in os.walk(filepath):
        for file in (i for i in files if ".ram" in i):
            print(directory, subdirectories, file)
            try:
                with open("{}/{}".format(directory, file), "r") as f:
                    url = f.read().strip()
            except:
                continue

            output_filepath = "{}/{}.{}".format(directory, file.strip(".ram"), url.split('.')[-1])
            edited_url = "http://{}".format(url.strip("rtsp://"))
            if not os.path.isfile(output_filepath):
                if ".mp3" in url:
                    r = requests.get(edited_url)
                    data = r.content
                    with open(output_filepath, "wb") as f:
                        f.write(data)
