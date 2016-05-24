#! /usr/bin/env python3

import os
import csv


def report_expected_objs(filename):
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        full_set_pointers = {'cpd': set(), 'simple': set()}

        headers = next(csv_reader)
        alias_col_num = headers.index('CONTENTdm number')
        filename_col_num = headers.index('CONTENTdm file name')

        for row in csv_reader:
            alias = row[alias_col_num]
            if alias not in ('CONTENTdm number'):
                filename = row[filename_col_num]
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
                if 'parent' in file:
                    continue
                if os.path.splitext(file)[-1].lower().replace('.', '') == 'json':
                    full_set_downloaded_pointers['cpd'].add(os.path.splitext(file)[0])

            if os.path.isdir(os.path.join(cached_alias_dir, 'Cpd', file)):
                for subfile in os.listdir(os.path.join(cached_alias_dir, 'Cpd', file)):
                    if os.path.splitext(subfile)[-1].lower().replace('.', '') == 'json':
                        if 'parent' in subfile:
                            continue
                        full_set_downloaded_pointers['simple'].add(os.path.splitext(subfile)[0])
    return full_set_downloaded_pointers

my_alias = 'FJC'
filepath = '/home/james/Desktop/txtExportfromCDM/{}.csv'.format(my_alias)

expected_sets = report_expected_objs(filepath)
print('AdminPanel Smpl Objs:', len(expected_sets['simple']))
print('AdminPanel Cmpd Objs:', len(expected_sets['cpd']))

pulled_sets = report_pulled_objs(my_alias)
print('WebApi Smpl Objs:', len(pulled_sets['simple']))
print('WebApi Cmpd Objs:', len(pulled_sets['cpd']))


print("AdminPanel extras Simple:", len(expected_sets['simple'].difference(pulled_sets['simple'])), expected_sets['simple'].difference(pulled_sets['simple']))
print('WebApi extras Simple:', len(pulled_sets['simple'].difference(expected_sets['simple'])), pulled_sets['simple'].difference(expected_sets['simple']))
print('AdminPanel extras Cpd:', len(expected_sets['cpd'].difference(pulled_sets['cpd'])), expected_sets['cpd'].difference(pulled_sets['cpd']))
print('WebApi extras Cpd:', len(pulled_sets['cpd'].difference(expected_sets['cpd'])), pulled_sets['cpd'].difference(expected_sets['cpd']))
