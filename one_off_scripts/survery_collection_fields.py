#! /usr/bin/env python3

import xmlify


coll_fields = dict()

for alias in xmlify.list_all_aliases():
    print(alias)
    for elem in xmlify.grab_collection_fields(alias).iter():
        if elem.tag == 'field':
            sought_tags = (tag.text for tag in elem.getchildren() if tag.tag == 'name')
            for sought_tag in sought_tags:
                if sought_tag not in coll_fields:
                    coll_fields[sought_tag] = []
                coll_fields[sought_tag].append(alias)

with open('survey_coll.txt', 'w') as f:
    f.write(str(coll_fields))
