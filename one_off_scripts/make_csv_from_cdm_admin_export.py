#! /usr/bin/env python3

#! /usr/bin/env python3

import sys
import os
import csv

found_pointers = set()


def report_expected_objs(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        print(filename)
        csv_reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        
        full_set_pointers = {'cpd': set(), 'simple': set()}

        headers = next(csv_reader)
        pointer_col_num = headers.index('CONTENTdm number')
        filename_col_num = headers.index('CONTENTdm file name')

        for num, row in enumerate(csv_reader):
            pointer = row[pointer_col_num]
            if pointer not in ('CONTENTdm number'):
                filename = row[filename_col_num]
                if os.path.splitext(filename)[-1].lower().replace('.', '') == ('cpd'):
                    full_set_pointers['cpd'].add(pointer)
                else:
                    full_set_pointers['simple'].add(pointer)
    return full_set_pointers


def check_csvs_for_corruption(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        print(filename)
        csv_reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        headers = next(csv_reader)
        pointer_col_num = headers.index('CONTENTdm number')

        for num, row in enumerate(csv_reader):
            pointer = row[pointer_col_num]
            if not pointer.isnumeric() or (len(pointer) == 0):
                print(pointer)




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


csv_dir = '/home/james/Desktop/txtExportfromCDM'
for file in os.listdir(csv_dir):
    if os.path.isfile(os.path.join(csv_dir, file)):
        fullpath = os.path.join(csv_dir, file)
        check_csvs_for_corruption(fullpath)
        expected_sets = report_expected_objs(fullpath)
    # pulled_sets = report_pulled_objs(file)

    # csv_simple_extras = expected_sets['simple'].difference(pulled_sets['simple'])
    # csv_cpd_extras = expected_sets['cpd'].difference(pulled_sets['cpd'])
    # print("AdminPanel extras Simple:",
    #       len(csv_simple_extras),
    #       csv_simple_extras)
    # print('AdminPanel extras Cpd:',
    #       len(csv_cpd_extras),
    #       csv_cpd_extras)

    # for item in csv_cpd_extras:
    #     pass
