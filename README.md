# cdm_xporter

pull_from_cdm.py is a collection of defs that pulls published data from a CONTENTdm repository.  Nearly all of a cdm repo can be pulled into xml through some combination of these defs.

xmlify.py is a group of functions useful for pulling all the metadata/binaries from a given collection into one xml per collection.  By default, "python3 xmlify" will result in all metadata for all collections converted to xml and saved on your computer.

Commenting/Uncommenting some lines will result in downloading binaries.  

git clone https://github.com/lsulibraries/cdm_xporter/
python3 xmlify

else, one can import the functions into other scripts for your custom project. 
