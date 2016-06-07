#! /usr/bin/env python3

import os
import csv
import lxml.etree as etree


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
    cached_alias_dir = os.path.join(os.pardir, os.pardir, 'Cached_Cdm_files', alias)
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

csv_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'txtExportfromCDM')

repo_admin_spl_extras = dict()
repo_admin_cmp_extras = dict()
repo_webapi_spl_extras = dict()
repo_webapi_cmp_extras = dict()
failed = []

for file in os.listdir(csv_dir):
    if os.path.isdir(file):
        continue
    filepath = os.path.join(csv_dir, file)
    alias = os.path.splitext(file)[0]
    print(alias)

    try:
        expected_sets = report_expected_objs(filepath)
        print('AdminPanel Smpl Objs:', len(expected_sets['simple']))
        print('AdminPanel Cmpd Objs:', len(expected_sets['cpd']))

        pulled_sets = report_pulled_objs(alias)
        print('WebApi Smpl Objs:', len(pulled_sets['simple']))
        print('WebApi Cmpd Objs:', len(pulled_sets['cpd']))

        admin_spl_extras = expected_sets['simple'].difference(pulled_sets['simple'])
        admin_cmp_extras = expected_sets['cpd'].difference(pulled_sets['cpd'])
        webapi_spl_extras = pulled_sets['simple'].difference(expected_sets['simple'])
        webapi_cmp_extras = pulled_sets['cpd'].difference(expected_sets['cpd'])

        print("AdminPanel extras Simple:", len(admin_spl_extras), admin_spl_extras)
        print('WebApi extras Simple:', len(webapi_spl_extras), webapi_spl_extras)
        print('AdminPanel extras Cpd:', len(admin_cmp_extras), admin_cmp_extras)
        print('WebApi extras Cpd:', len(webapi_cmp_extras), webapi_cmp_extras)

        if admin_spl_extras:
            repo_admin_spl_extras[alias] = admin_spl_extras
        if admin_cmp_extras:
            repo_admin_cmp_extras[alias] = admin_cmp_extras
        if webapi_spl_extras:
            repo_webapi_spl_extras[alias] = webapi_spl_extras
        if webapi_cmp_extras:
            repo_webapi_cmp_extras[alias] = webapi_cmp_extras
    except:
        failed.append(file)
        print('oops')

print('repo_admin_spl_extras', repo_admin_spl_extras)
print('repo_admin_cmp_extras', repo_admin_cmp_extras)
print('repo_webapi_spl_extras', repo_webapi_spl_extras)
print('repo_webapi_cmp_extras', repo_admin_cmp_extras)


print('failed', failed)
