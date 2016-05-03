#! /usr/bin/env python3

'''
This is a dev .py file that imitates pull_from_cdm -- without making calls to the contentdm url
'''

import os


def retrieve_collections_list():
    with open('Collections/Collections_List.xml', 'r') as f:
        return f.read()


def retrieve_collection_metadata(collection_alias):
    with open('Collections/{}/Collection_Metadata.xml'.format(collection_alias), 'r') as f:
        return f.read()


def retrieve_collection_total_recs(collection_alias):
    with open('Collections/{}/Collection_TotalRecs.xml'.format(collection_alias), 'r') as f:
        return f.read()


def retrieve_collection_fields(collection_alias):
    with open('Collections/{}/Collection_Fields.xml'.format(collection_alias), 'r') as f:
        return f.read()


def retrieve_elems_in_collection(collection_alias, fields_list, starting_pointer):
    with open('Collections/{}/Elems_in_Collection_{}.xml'.format(collection_alias, starting_pointer), 'r') as f:
        return f.read()


def retrieve_item_metadata(collection_alias, item_pointer):
    with open('Collections/{}/{}.xml'.format(collection_alias, item_pointer), 'r') as f:
        return f.read()


def retrieve_binaries(collection_alias, item_pointer, filetype):
    with open('Collections/{}/{}.{}'.format(collection_alias, item_pointer, filetype), 'rb') as f:
        return f.read()


def retrieve_compound_object(collection_alias, item_pointer):
    with open('Collections/{}/{}}.xml'.format(collection_alias, item_pointer), 'r') as f:
        return f.read()


def write_binary_to_file(binary, alias, new_filename, filetype):
    os.makedirs('Sourced_from_HD_Collections/{}'.format(alias), exist_ok=True)
    filename = 'Sourced_from_HD_Collections/{}/{}.{}'.format(alias, new_filename, filetype)
    with open(filename, 'bw') as f:
        f.write(binary)


def write_xml_to_file(xml_text, alias, new_filename):
    os.makedirs('Sourced_from_HD_Collections/{}'.format(alias), exist_ok=True)
    filename = 'Sourced_from_HD_Collections/{}/{}.xml'.format(alias, new_filename)
    with open(filename, 'w') as f:
        f.write(xml_text)


if __name__ == '__main__':
    pass
