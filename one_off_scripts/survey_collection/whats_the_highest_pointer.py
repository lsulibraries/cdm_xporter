#! /usr/bin/env python3

import os
import sys
sys.path.append("..")
import xmlify

os.chdir('..')

coll_list_txt = xmlify.list_all_aliases()
print(coll_list_txt)


highest_alias = 0

for alias in coll_list_txt:
    print(alias)
    if alias in ('p16313coll98'):
        continue
    for known_file in os.listdir('{}/March1Pull/Collections/{}'.format(os.getcwd(), alias)):
        known_file = known_file[:-4]
        if known_file.isnumeric():
            if int(highest_alias) < int(known_file):
                highest_alias = int(known_file)
                print(highest_alias)

print(highest_alias)

# output included pointer 307771 in alias p120701coll25
 