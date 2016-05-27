#! /usr/bin/env python3

import os
import csv
import lxml.etree as etree
from retrying import retry

import pull_from_cdm_for_mik as p


def read_file(filename):
    with open(filename) as f:
        return f.read()

def get_everything(alias, alias_dir, pointer_tuple):
    set_of_cpd_simples = set()

    # write all compounds
    for pointer in pointer_tuple:
        filetype = lookup_filetype(alias, alias_dir, pointer)
        print('first part:', pointer, filetype)

        if filetype == 'cpd':
            os.makedirs('{}/Cpd'.format(alias_dir), exist_ok=True)

            if not os.path.isfile('{}/Cpd/{}_parent.xml'.format(alias_dir, pointer)):
                parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                p.write_admin_xml_to_file(parent_xml, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

            if not os.path.isfile('{}/Cpd/{}_parent.json'.format(alias_dir, pointer)):
                parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                p.write_admin_json_to_file(parent_json, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

            if not os.path.isfile('{}/Cpd/{}.json'.format(alias_dir, pointer)):
                item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                p.write_admin_json_to_file(item_json, '{}/Cpd'.format(alias), pointer)

            if not os.path.isfile('{}/Cpd/{}.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                p.write_admin_xml_to_file(item_xml, '{}/Cpd'.format(alias), pointer)

            if not os.path.isfile('{}/Cpd/{}_cpd.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_compound_object(alias, pointer)
                p.write_admin_xml_to_file(item_xml, '{}/Cpd'.format(alias), '{}_cpd'.format(pointer))

            item_xml_filepath = '{}/Cpd/{}_cpd.xml'.format(alias_dir, pointer)
            item_etree = etree.parse(item_xml_filepath)
            for i in item_etree.findall('.//pageptr'):
                set_of_cpd_simples.add(i.text)
            print('did all part 1')

    # write all simples not in compound
    for pointer in pointer_tuple:
        filetype = lookup_filetype(alias, alias_dir, pointer)
        print('second part', pointer, filetype)


        if (filetype != 'cpd') and (pointer not in set_of_cpd_simples):

            if not os.path.isfile('{}/{}_parent.xml'.format(alias_dir, pointer)):
                parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                p.write_admin_xml_to_file(parent_xml, alias, '{}_parent'.format(pointer))

            if not os.path.isfile('{}/{}_parent.json'.format(alias_dir, pointer)):
                parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                p.write_admin_json_to_file(parent_json, alias, '{}_parent'.format(pointer))

            if not os.path.isfile('{}/{}.json'.format(alias_dir, pointer)):
                item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                p.write_admin_json_to_file(item_json, alias, pointer)

            if not os.path.isfile('{}/{}.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                p.write_admin_xml_to_file(item_xml, alias, pointer)

            item_xml_filepath = '{}/{}.xml'.format(alias_dir, pointer)
            item_etree = etree.parse(item_xml_filepath)
            if item_etree.find('find') is not None:  # "find" is contentdm's abbr for 'file name'
                if not os.path.isfile('{}/{}.{}'.format(alias_dir, pointer, filetype)):
                    binary = p.retrieve_binaries(alias, pointer, "_")
                    p.write_admin_binary_to_file(binary, alias, pointer, filetype)
                    print('wrote', alias, pointer, filetype)
            print('did all part 2')

    # write all simples inside a compound
    if 'Cpd' in os.listdir(alias_dir):
        print('third part')

        for file in os.listdir(os.path.join(alias_dir, 'Cpd')):
            if '_cpd.xml' in file:
                cpd_pointer = file.split('_')[0]
                small_etree = etree.parse(os.path.join(alias_dir, 'Cpd', file))
                subpointer_list = small_etree.findall('.//pageptr')
                file_element = subpointer_list[0].getparent().xpath('./pagefile')
                if file_element and 'pdfpage' in file_element[0].text:
                    continue  # we don't want pdfpage objects
                os.makedirs('{}/Cpd/{}'.format(alias_dir, cpd_pointer), exist_ok=True)
                for elem in subpointer_list:
                    simple_pointer = elem.text

                    if not os.path.isfile('{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                        item_xml = p.retrieve_item_metadata(alias, simple_pointer, 'xml')
                        p.write_admin_xml_to_file(item_xml, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                    else:
                        item_xml = read_file('{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                        item_json = p.retrieve_item_metadata(alias, simple_pointer, 'json')
                        p.write_admin_json_to_file(item_json, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}_parent.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                        parent_xml = p.retrieve_parent_info(alias, simple_pointer, 'xml')
                        p.write_admin_xml_to_file(parent_xml, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))

                    if not os.path.isfile('{}/Cpd/{}/{}_parent.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                        parent_json = p.retrieve_parent_info(alias, simple_pointer, 'json')
                        p.write_admin_json_to_file(parent_json, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))

                    simple_etree = etree.fromstring(bytes(bytearray(item_xml, encoding='utf-8')))
                    orig_filename = simple_etree.find('find').text
                    simple_filetype = os.path.splitext(orig_filename)[-1].replace('.', '')
                    if not os.path.isfile('{}/Cpd/{}/{}.{}'.format(alias_dir, cpd_pointer, simple_pointer, simple_filetype)):
                        binary = p.retrieve_binaries(alias, simple_pointer, "arbitary")
                        simple_filepath = 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer)
                        p.write_admin_binary_to_file(binary, alias, simple_filepath, simple_filetype)
                        print('wrote', alias, cpd_pointer, simple_pointer, simple_filetype)
                    print('did all part 3')

def lookup_filetype(alias, alias_dir, pointer):
    for root, subdirs, files in os.walk(alias_dir):
        for file in files:
            if '{}.xml'.format(pointer) == file:
                item_etree = etree.parse(os.path.join(root, '{}.xml'.format(pointer)))
                filename = item_etree.find('find').text
                extension = os.path.splitext(filename)[-1].replace('.', '')
                print('1')
                return extension

    item_etree = etree.fromstring(bytes(bytearray(p.retrieve_item_metadata(alias, pointer, 'xml'), encoding='utf-8')))
    filename = item_etree.find('find').text
    extension = os.path.splitext(filename)[-1].replace('.', '')
    print('2')
    return extension

def report_expected_objs(filepath):
    with open(filepath, 'r') as f:
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
    cached_alias_dir = os.path.join('Cached_Cdm_files', alias)
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


if __name__ == '__main__':

    coll_list_txt = p.retrieve_collections_list()
    coll_list_xml = etree.fromstring(bytes(bytearray(coll_list_txt, encoding='utf-8')))
    not_all_binaries = []
    for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
        try:
            print(alias)

            alias_csv = '{}.csv'.format(alias)
            csv_filepath = os.path.join(os.path.pardir, 'txtExportfromCDM', alias_csv)
            expected_sets = report_expected_objs(csv_filepath)
            pulled_sets = report_pulled_objs(alias)

            sought_pointers = tuple(expected_sets['cpd'].difference(pulled_sets['cpd']).union(
                                    expected_sets['simple'].difference(pulled_sets['simple'])))
            print(sought_pointers)

            alias_dir = os.path.join('AdminPanel_Cdm_files', alias)
            os.makedirs(alias_dir, exist_ok=True)
            print((alias, alias_dir, sought_pointers))
            # get_everything(alias, alias_dir, sought_pointers)

        except:
            not_all_binaries.append(alias)
            print('oops')
    print(not_all_binaries)
