#! /usr/bin/env python3

import os
import re
import lxml.etree as etree

import pull_from_cdm_for_mik as p


def read_file(filename):
    with open(filename) as f:
        return f.read()


def just_so_i_can_call_it(alias):
    repo_dir = os.path.join('..', 'Cached_Cdm_files')
    alias_dir = '{}/{}'.format(repo_dir, alias)

    os.makedirs(alias_dir, exist_ok=True)

    if not os.path.isfile('{}/Collection_Metadata.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_metadata(alias),
            alias,
            'Collection_Metadata')

    if not os.path.isfile('{}/Collection_TotalRecs.xml'.format(alias_dir)):
        p.write_xml_to_file(
            p.retrieve_collection_total_recs(alias),
            alias,
            'Collection_TotalRecs')

    if not os.path.isfile('{}/Collection_Fields.json'.format(alias_dir)):
        collection_fields_json = p.retrieve_collection_fields_json(alias)
        p.write_json_to_file(
            collection_fields_json,
            alias,
            'Collection_Fields')

    if not os.path.isfile('{}/Collection_Fields.xml'.format(alias_dir)):
        collection_fields_xml = p.retrieve_collection_fields_xml(alias)
        p.write_xml_to_file(
            collection_fields_xml,
            alias,
            'Collection_Fields')
    else:
        collection_fields_xml = read_file(
            '{}/Collection_Fields.xml'.format(alias_dir))

    total_recs_etree = etree.parse(os.path.join(alias_dir, 'Collection_TotalRecs.xml'))
    num_of_pointers = int(total_recs_etree.xpath('.//total')[0].text)
    groups_of_100 = (num_of_pointers // 100) + 1

    for num in range(groups_of_100):
        starting_pointer = (num * 100) + 1
        if not os.path.isfile('{}/Elems_in_Collection_{}.xml'.format(alias_dir, starting_pointer)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            xml_elems_in_coll = p.retrieve_elems_xml(alias, fields_to_retrieve, starting_pointer)
            p.write_xml_to_file(
                xml_elems_in_coll,
                alias,
                'Elems_in_Collection_{}'.format(starting_pointer))

        elems_in_coll_tree = etree.parse(
            '{}/Elems_in_Collection_{}.xml'.format(alias_dir, starting_pointer))

        if not os.path.isfile('{}/Elems_in_Collection_{}.json'.format(alias_dir, starting_pointer)):
            fields_to_retrieve = ['source', 'dmrecord', 'dmimage', 'find']
            json_elems_in_coll = p.retrieve_elems_json(alias, fields_to_retrieve, starting_pointer)
            p.write_json_to_file(
                json_elems_in_coll,
                alias,
                'Elems_in_Collection_{}'.format(starting_pointer))

        pointers_filetypes = [(single_record.find('dmrecord').text,
                               single_record.find('filetype').text,
                               ) for single_record in elems_in_coll_tree.findall('.//record')]

        for pointer, filetype in pointers_filetypes:
            if not pointer:
                continue  # skips file if a derivative -- only gets original versions
            print(alias, pointer, filetype)
            if filetype != 'cpd':

                if not os.path.isfile('{}/{}.json'.format(alias_dir, pointer)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, alias, pointer)

                if not os.path.isfile('{}/{}.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, alias, pointer)

                if not os.path.isfile('{}/{}_parent.xml'.format(alias_dir, pointer)):
                    parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                    p.write_xml_to_file(parent_xml, alias, '{}_parent'.format(pointer))

                if not os.path.isfile('{}/{}_parent.json'.format(alias_dir, pointer)):
                    parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                    p.write_json_to_file(parent_json, alias, '{}_parent'.format(pointer))

                item_xml_filepath = '{}/{}.xml'.format(alias_dir, pointer)
                item_etree = etree.parse(item_xml_filepath)
                if item_etree.find('find') is not None:  # "find" is contentdm's abbr for 'file name'
                    if not os.path.isfile('{}/{}.{}'.format(alias_dir, pointer, filetype)):
                        try:
                            binary = p.retrieve_binaries(alias, pointer, "_")
                            p.write_binary_to_file(binary, alias, pointer, filetype)
                            print('wrote', alias, pointer, filetype)
                        except:
                            broken_pointers.add(pointer)
                            continue

            elif filetype == 'cpd':
                os.makedirs('{}/Cpd'.format(alias_dir), exist_ok=True)

                if not os.path.isfile('{}/Cpd/{}.json'.format(alias_dir, pointer)):
                    item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                    p.write_json_to_file(item_json, '{}/Cpd'.format(alias), pointer)

                if not os.path.isfile('{}/Cpd/{}.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                    p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), pointer)

                if not os.path.isfile('{}/Cpd/{}_parent.xml'.format(alias_dir, pointer)):
                    parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                    p.write_xml_to_file(parent_xml, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

                if not os.path.isfile('{}/Cpd/{}_parent.json'.format(alias_dir, pointer)):
                    parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                    p.write_json_to_file(parent_json, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

                item_xml_filepath = '{}/Cpd/{}.xml'.format(alias_dir, pointer)
                item_etree = etree.parse(item_xml_filepath)

                if not os.path.isfile('{}/Cpd/{}_cpd.xml'.format(alias_dir, pointer)):
                    item_xml = p.retrieve_compound_object(alias, pointer)
                    p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), '{}_cpd'.format(pointer))


    if 'Cpd' in os.listdir(alias_dir):
        for file in os.listdir(os.path.join(alias_dir, 'Cpd')):
            # if file[0] != '9':
            #     continue
            if os.path.isfile(os.path.join(alias_dir, 'Cpd', file)):

                # retrying hack to get pdf at compound root of known collections
                if alias in ('p16313coll5', 'p15140coll7', 'p15140coll42', 'p15140coll44', 'p15140coll49', 'p15140coll50', 'p16313coll91',
                    'p16313coll95', 'p16313coll98', 'p120701coll12', 'p120701coll26', 'LOYOLA_ETD', 'LOYOLA_ETDa', 'LOYOLA_ETDb', 'lapur',):
                    match = re.search(r'[0-9]+.xml', file)
                    # if match:
                    if file == '25303.xml':
                        root_cpd_etree = etree.parse(os.path.join(alias_dir, 'Cpd', file))
                        pointer = root_cpd_etree.findall('.//dmrecord')[0].text
                        filetype = root_cpd_etree.findall('.//format')[0].text
                        if not os.path.isfile('{}/Cpd/{}.{}'.format(alias_dir, pointer, filetype)):
                            try:
                                binary = p.retrieve_binaries(alias, pointer, filetype)
                                try:
                                    binary.decode('utf-8')
                                    print(alias, pointer)
                                    print('normal xxx_cpd.xml isnt a binary at root')
                                except:
                                    root_cpd_filepath = 'Cpd/{}'.format(pointer)
                                    p.write_binary_to_file(binary, alias, root_cpd_filepath, 'pdf')
                                    print(root_cpd_filepath, 'wrote root binary')
                                    continue
                            except: 
                                incomplete_collection.append((alias, pointer))
                if '_cpd.xml' in file:
                    print(file)
                    cpd_pointer = file.split('_')[0]
                    small_etree = etree.parse(os.path.join(alias_dir, 'Cpd', file))
                    subpointer_list = small_etree.findall('.//pageptr')
                    file_element = subpointer_list[0].getparent().xpath('./pagefile')
                    if file_element and 'pdfpage' in file_element[0].text:
                        continue  # we don't want pdfpage objects
                    os.makedirs('{}/Cpd/{}'.format(alias_dir, cpd_pointer), exist_ok=True)
                    for elem in subpointer_list:
                        simple_pointer = elem.text
                        print(simple_pointer)

                        if not os.path.isfile('{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                            item_xml = p.retrieve_item_metadata(alias, simple_pointer, 'xml')
                            p.write_xml_to_file(item_xml, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                        else:
                            item_xml = read_file(
                                '{}/Cpd/{}/{}.xml'.format(alias_dir, cpd_pointer, simple_pointer))

                        if not os.path.isfile('{}/Cpd/{}/{}.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                            item_json = p.retrieve_item_metadata(alias, simple_pointer, 'json')
                            p.write_json_to_file(item_json, alias, 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer))

                        if not os.path.isfile('{}/Cpd/{}/{}_parent.xml'.format(alias_dir, cpd_pointer, simple_pointer)):
                            parent_xml = p.retrieve_parent_info(alias, simple_pointer, 'xml')
                            p.write_xml_to_file(parent_xml, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))

                        if not os.path.isfile('{}/Cpd/{}/{}_parent.json'.format(alias_dir, cpd_pointer, simple_pointer)):
                            parent_json = p.retrieve_parent_info(alias, simple_pointer, 'json')
                            p.write_json_to_file(parent_json, alias, 'Cpd/{}/{}_parent'.format(cpd_pointer, simple_pointer))

                        simple_etree = etree.fromstring(bytes(bytearray(item_xml, encoding='utf-8')))
                        try:
                            orig_filename = simple_etree.find('find').text
                            simple_filetype = os.path.splitext(orig_filename)[-1].replace('.', '')
                            if not os.path.isfile('{}/Cpd/{}/{}.{}'.format(alias_dir, cpd_pointer, simple_pointer, simple_filetype)):
                                try:
                                    binary = p.retrieve_binaries(alias, simple_pointer, "arbitary")
                                    simple_filepath = 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer)
                                    print(simple_filepath)
                                    p.write_binary_to_file(binary, alias, simple_filepath, simple_filetype)
                                    print('wrote', alias, cpd_pointer, simple_pointer, simple_filetype)
                                except:
                                    print('failed to grab, excepting')
                        except:
                            print('not real xml', file)
                            broken_pointers.add((cpd_pointer, simple_pointer))




if __name__ == '__main__':
    """ Call just one collection, retrieve all metadata """
    incomplete_collection = []
    for alias in ('LSUHSC_NCC', ):
        print(alias)
        broken_pointers = set()
        just_so_i_can_call_it(alias)
        incomplete_collection.append('{} {}'.format(alias, broken_pointers))
    print('Reason: LSUHSC_NCC still missing binaries for whatever reason')
    print(incomplete_collection)


    """ Call all collections, retrieve all metadata """

    we_dont_migrate = {'p16313coll70', 'p120701coll11', 'LSUHSCS_JCM', 'UNO_SCC', 'p15140coll36', 'p15140coll57',
                       'p15140coll13', 'p15140coll11', 'p16313coll32', 'p16313coll49', 'p16313coll50',
                       'p16313coll90', 'p120701coll14', 'p120701coll20', 'p120701coll21', 'DUBLIN2',
                       'HHN', 'p15140coll55', 'NOD', 'WIS', 'p16313coll55', 'LOU_RANDOM', 'p120701coll11',
                       'p16313coll67', 'AMA', 'HTU', 'p15140coll3', 'p15140coll15', 'p15140coll25',
                       'p15140coll29', 'p15140coll34', 'p15140coll37', 'p15140coll38', 'p15140coll39',
                       'p15140coll40', 'p15140coll45', 'p15140coll47', 'p15140coll58', 'p16313coll4',
                       'p16313coll6', 'p16313coll11', 'p16313coll12', 'p16313coll13', 'p16313coll14',
                       'p16313coll15', 'p16313coll16', 'p16313coll29', 'p16313coll27', 'p16313coll30',
                       'p16313coll33', 'p16313coll37', 'p16313coll38', 'p16313coll39', 'p16313coll41',
                       'p16313coll42', 'p16313coll46', 'p16313coll47', 'p16313coll53', 'p16313coll59',
                       'p16313coll63', 'p16313coll64', 'p16313coll66', 'p16313coll68', 'p16313coll71',
                       'p16313coll73', 'p16313coll75', 'p16313coll78', 'p16313coll84',
                       'p15140coll32', 'p16313coll82', 'p120701coll6', 'p267101coll4',
                       'p16313coll44', 'p16313coll88', 'p16313coll94', 'JSN', 'p15140coll24',
                       'p15140coll9', 'p15140coll59', 'p16313coll40', 'p15140coll53', 'p16313coll97',
                       'p16313coll18', 'p15140coll33', 'LST', 'MPF', 'p15140coll2', }

    # repo_dir = '../Cached_Cdm_files'
    # if not os.path.isfile(os.path.join(repo_dir, 'Collections_List.xml')):
    #     coll_list_txt = p.retrieve_collections_list()
    #     p.write_xml_to_file(coll_list_txt, '.', 'Collections_List')
    #     coll_list_xml = etree.fromstring(bytes(bytearray(coll_list_txt, encoding='utf-8')))
    # else:
    #     coll_list_xml = etree.parse(os.path.join(repo_dir, 'Collections_List.xml'))
    # not_all_binaries = []
    # for alias in [alias.text.strip('/') for alias in coll_list_xml.findall('.//alias')]:
    #     broken_pointers = set()
    #     if alias in we_dont_migrate:
    #         continue
    #     # try:
    #     #     print('{} '.format(alias) * 10)
    #     just_so_i_can_call_it(alias)
    #     # except:
    #     #     not_all_binaries.append((alias, broken_pointers))
    #     print(alias)
    #     print(broken_pointers)
    # print(not_all_binaries)
