# cdm_xporter

pull_from_cdm.py is a collection of defs that pulls published data from a CONTENTdm repository (unless CONTENTdm failed at indexing your repository -- then all bets are off).  Nearly all of a cdm repo can be pulled into xml through some combination of these defs.

quick_simple_collection_query.py can pull all the xmls (or only the ones you don't comment out).  It saves them in a folder within the project folder, as one xml per each simple_object, one xml describing the compound_objects' metadata, and one xml describing the collection's metadata.  It only calls one collection per run, which you specify within the script.  It also pulls all binaries in the collection (again, unless you comment this out).

xmlify.py is a group of functions useful for pulling all the metadata/binaries within a repositoty into one xml per collection.  Binaries are also grabbed, unless commented out.  Any   By default, "python3 xmlify" will result in all metadata for all collections converted to xml (and all binaries) saved on your computer.  PS, your computer is not big enough; be careful with this script.  On a nice note, if the script finds an xml for a collection already on your computer, it will skip forward to the next collection.  


git clone https://github.com/lsulibraries/cdm_xporter/

python3 xmlify

else, one can import the functions into other scripts for your custom project. 
