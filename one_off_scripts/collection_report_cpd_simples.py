#! /usr/bin/env python3

import os
import csv


def report_expected_objs(filename):
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        full_set_pointers = {'cpd': set(), 'simple': set()}

        for row in csv_reader:
            alias = row[0]
            if alias not in ('CONTENTdm number'):
                filename = row[1]
                if os.path.splitext(filename)[-1].lower().replace('.', '') == ('cpd'):
                    full_set_pointers['cpd'].add(alias)
                else:
                    full_set_pointers['simple'].add(alias)

    return full_set_pointers


def report_pulled_objs(alias):
    cached_alias_dir = os.path.join(os.path.pardir, 'Cached_Cdm_files', alias)
    full_set_downloaded_pointers = {'cpd': set(), 'simple': set()}

    for file in os.listdir(cached_alias_dir):
        if os.path.splitext(file)[-1].lower().replace('.', '') == 'xml':
            if os.path.splitext(file)[0].isnumeric():
                full_set_downloaded_pointers['simple'].add(os.path.splitext(file)[0])

    if os.path.exists(os.path.join(cached_alias_dir, 'Cpd')):
        for file in os.listdir(os.path.join(cached_alias_dir, 'Cpd')):

            if os.path.isfile(os.path.join(cached_alias_dir, 'Cpd', file)):
                if os.path.splitext(file)[-1].lower().replace('.', '') == 'json':
                    full_set_downloaded_pointers['cpd'].add(os.path.splitext(file)[0])

            if os.path.isdir(os.path.join(cached_alias_dir, 'Cpd', file)):
                for subfile in os.listdir(os.path.join(cached_alias_dir, 'Cpd', file)):
                    if os.path.splitext(subfile)[-1].lower().replace('.', '') == 'json':
                        full_set_downloaded_pointers['simple'].add(os.path.splitext(subfile)[0])
    return full_set_downloaded_pointers


# expected_sets = report_expected_objs('/home/garrett_armstrong/Desktop/lapur_items.csv')
# print(len(expected_sets['simple']))
# print(len(expected_sets['cpd']))

pulled_sets = report_pulled_objs('CLF')
print(len(pulled_sets['simple']))
print(len(pulled_sets['cpd']))


# print("Them minus us Simple", expected_sets['simple'].difference(pulled_sets['simple']))
# print('Us minus them Simple', pulled_sets['simple'].difference(expected_sets['simple']))
# print('Them minus us Cpd', expected_sets['cpd'].difference(pulled_sets['cpd']))
# print('Us minus them Cpd', pulled_sets['cpd'].difference(expected_sets['cpd']))
