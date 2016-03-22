#! /usr/bin/env python3

import os
import sys
import csv

sys.path.append("..")
import quick_simple_collection_query


os.chdir('..')


def expected_number_of_pointers(name):
    with open('one_off_scripts/NumberAndTypeAllLDL.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            if name == row[0]:
                return row[3]


def write_missing_pointers_status():
    with open('Collections_Expected_vs_Grabbed.txt', 'w') as f:
        for item in incomplete_collections:
            f.write('{}\n'.format(item))


alias_name = []
incomplete_collections = []


with open('one_off_scripts/Alias_Name_Description.csv', 'r') as f:
    file_text = f.read()
    for line in file_text.splitlines():
        line = line[0:line.find('<p>')]
        if "No descriptio" in line:
            line = line.replace('No descriptio', '')
        alias = line[0:line.find(' ')]
        name = line[line.find(' '):]
        if alias and name:
            alias_name.append((alias.strip(), name.strip()))


for alias, name in alias_name:
    number_grabbed = len([
                         filename for filename in os.listdir('Collections/{}'.format(alias)) 
                         if filename not in ('Collection_Fields.xml', 'Collection_Metadata.xml', 'Elems_in_Collection.xml')
                         ])
    number_expected = expected_number_of_pointers(name)
    if number_expected and number_grabbed:
        number_expected, number_grabbed = int(number_expected), int(number_grabbed)
        if number_grabbed != number_expected:
            print(alias, name, number_expected, number_grabbed)
            incomplete_collections.append((alias, name, number_expected, number_grabbed))
            write_missing_pointers_status()
            quick_simple_collection_query.success_checker(alias, int(number_expected - number_grabbed))
    else:
        print('ERROR: {} {}'.format(alias, name))
        incomplete_collections.append('ERROR: {} {}'.format(alias, name))

incomplete_collections = sorted(incomplete_collections, key=lambda x: x[0])
write_missing_pointers_status()




