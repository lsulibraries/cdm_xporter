# cdm_xporter

Before using these scripts, consider using https://github.com/MarcusBarnes/mik.  Their created a suite of software for migrating from contentDM to Islandora.


scrape_cDM.py pulls all the necessary binaries and metadata for converting to mods & migration to Islandora.  There are two sections in the `if __name__ == '__main__':`.  The first allows you to specify certain collections to scrape.  The second allows you to pull all aliases, except those you specify.  


cDM_api_call.py is merely a group of contentDM API calls we frequently used.  It's useful as an import.  You will want to change the string specifying your contentDM server address.


`git clone https://github.com/lsulibraries/cdm_xporter/`

`python3 scrape_cDM`

look for the output in "../Cached_Cdm_files"
