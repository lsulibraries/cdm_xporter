#! /usr/bin/env python3

import os
import sys
import csv

sys.path.append("..")
# import quick_simple_collection_query
import lxml.etree as ET

os.chdir('..')


def write_missing_pointers_status():
    with open('Collections_Expected_vs_Grabbed.txt', 'w') as f:
        for item in incomplete_collections:
            f.write('{}\n'.format(item))

def in_house_number_of_pointers(coll_name):
    with open('one_off_scripts/NumberAndTypeAllLDL.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            if coll_name == row[0]:
                return int(row[3]) - int(row[4])
    return None

def get_in_house_list_of_collections():
    with open('one_off_scripts/NumberAndTypeAllLDL.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        collection_list = []
        for row in csv_reader:
            collection_list.append(row[0])
    return collection_list


def cdm_reported_number_of_pointers(alias):
    with open('Collections/{}/Collection_TotalRecs.xml'.format(alias), 'r') as f:
        f_read = bytes(bytearray(f.read(), encoding='utf-8'))
        f_etree = ET.fromstring(f_read)
    for elem in f_etree.iter():
        if elem.tag == 'total':
            return int(elem.text)

def make_alias_name_list():
    alias_name = []
    with open('{}/Collections/Collections_List.xml'.format(os.getcwd()), 'r') as f:
        f_read = bytes(bytearray(f.read(), encoding='utf-8'))
        f_etree = ET.fromstring(f_read)
    for coll in f_etree.xpath('.//collection'):
        for item in coll.iterchildren():
            if item.tag == 'alias':
                alias = item.text.replace('/', '').strip()
            if item.tag == 'name':
                name = item.text.strip()
        alias_name.append((alias, name))
    return alias_name

def count_alias_objects_compounds(alias):
    count = 0
    compound = 0
    for filename in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
        if 'Elems_in_Collection' in filename:
            with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, filename)) as f:
                f_read = bytes(bytearray(f.read(), encoding='utf-8'))
                f_etree = ET.fromstring(f_read)
            for elem in f_etree.xpath('.//record'):
                for subelem in elem.iter():
                    if subelem.tag == 'dmrecord':
                        if subelem.text:
                            count += 1
                    if subelem.tag == 'filetype':
                        if subelem.text in ('cpd'):
                            compound += 1
    return (alias, count, compound)

def report_inhouse_versus_grabbed_minus_cpd(packaged_up):
    (in_house_number, cdm_reported_number, number_grabbed, number_cpd_grabbed, alias, name) = packaged_up
    if in_house_number == cdm_reported_number == (number_grabbed - number_cpd_grabbed):
        print('{}         \tcompletely grabbed'.format(alias))
    elif cdm_reported_number != number_grabbed:
        return (
            'Grabbed:\t{}\tCDM:\t{}\tHouse:\t{}\tAlias:\t{}\tName:\t{}'.format(
                (number_grabbed - number_cpd_grabbed),
                cdm_reported_number,
                in_house_number,
                alias,
                name)
            )

def report_all_status(packaged_up):
    (in_house_number, cdm_reported_number, number_grabbed, number_cpd_grabbed, alias, name) = packaged_up
    return (
            'All Grabbed:\t{}\tGrabbed cpd:\t{}\tCDM:\t{}\tHouse:\t{}\tAlias:\t{}\tName:\t{}'.format(
                number_grabbed,
                number_cpd_grabbed,
                cdm_reported_number,
                in_house_number,
                alias,
                name)
            )

# if __name__ == '__main__':
#     in_house_list = get_in_house_list_of_collections()
#     print(in_house_list)


if __name__ == '__main__':
    incomplete_collections = []
    for alias, name in make_alias_name_list():
        if alias and name:
            number_grabbed = int(len([
                filename for filename in os.listdir('Collections/{}'.format(alias))
                if filename[:-4].isnumeric()
                ]))
            number_cpd_grabbed = count_alias_objects_compounds(alias)[2]
            in_house_number = in_house_number_of_pointers(name)
            cdm_reported_number = int(cdm_reported_number_of_pointers(alias))
            packaged_up = (in_house_number, cdm_reported_number, number_grabbed, number_cpd_grabbed, alias, name)
            # incomplete_collections.append(report_inhouse_versus_grabbed_minus_cpd(packaged_up))
            incomplete_collections.append(report_all_status(packaged_up))
        else:
            print('{} something missing an alias or name'.format(alias))

    incomplete_collections = sorted(incomplete_collections, key=lambda x: x[0])
    write_missing_pointers_status()
