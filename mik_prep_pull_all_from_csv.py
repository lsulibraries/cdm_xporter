#! /usr/bin/env python3

import os
import lxml.etree as etree
from retrying import retry

import pull_from_cdm_for_mik as p

#   expects (('p16313coll7', (('311', 'jpg'), ('324', 'png'), )
def get_everything(alias, pointerfiletype_tuple):
    repo_dir = '{}/{}'.format(os.getcwd(), 'AdminPanel_Cdm_files')
    alias_dir = '{}/{}'.format(repo_dir, alias)
    os.makedirs(alias_dir, exist_ok=True)

    for pointer, filetype in pointerfiletype_tuple:

        if filetype == 'cpd':
            os.makedirs('{}/Cpd'.format(alias_dir), exist_ok=True)

            if not os.path.isfile('{}/Cpd/{}_parent.xml'.format(alias_dir, pointer)):
                parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                p.write_xml_to_file(parent_xml, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

            if not os.path.isfile('{}/Cpd/{}_parent.json'.format(alias_dir, pointer)):
                parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                p.write_json_to_file(parent_json, '{}/Cpd'.format(alias), '{}_parent'.format(pointer))

            if not os.path.isfile('{}/Cpd/{}.json'.format(alias_dir, pointer)):
                item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                p.write_json_to_file(item_json, '{}/Cpd'.format(alias), pointer)

            if not os.path.isfile('{}/Cpd/{}.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), pointer)

            item_xml_filepath = '{}/Cpd/{}.xml'.format(alias_dir, pointer)
            item_etree = etree.parse(item_xml_filepath)

            if not os.path.isfile('{}/Cpd/{}_cpd.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_compound_object(alias, pointer)
                p.write_xml_to_file(item_xml, '{}/Cpd'.format(alias), '{}_cpd'.format(pointer))

        elif (filetype != 'cpd') and ('{}.xml'.format(pointer) not in os.walk(alias_dir)):

            if os.path.isfile('{}/{}_parent.xml'.format(alias_dir, pointer)):
                pointer_parent_info_xml = etree.parse('{}/{}.xml'.format(alias_dir, pointer))
                print(pointer_parent_info_xml)

            if not os.path.isfile('{}/{}_parent.xml'.format(alias_dir, pointer)):
                parent_xml = p.retrieve_parent_info(alias, pointer, 'xml')
                p.write_xml_to_file(parent_xml, alias, '{}_parent'.format(pointer))

            if not os.path.isfile('{}/{}_parent.json'.format(alias_dir, pointer)):
                parent_json = p.retrieve_parent_info(alias, pointer, 'json')
                p.write_json_to_file(parent_json, alias, '{}_parent'.format(pointer))

            if not os.path.isfile('{}/{}.json'.format(alias_dir, pointer)):
                item_json = p.retrieve_item_metadata(alias, pointer, 'json')
                p.write_json_to_file(item_json, alias, pointer)

            if not os.path.isfile('{}/{}.xml'.format(alias_dir, pointer)):
                item_xml = p.retrieve_item_metadata(alias, pointer, 'xml')
                p.write_xml_to_file(item_xml, alias, pointer)



            item_xml_filepath = '{}/{}.xml'.format(alias_dir, pointer)
            item_etree = etree.parse(item_xml_filepath)
            if item_etree.find('find') is not None:  # "find" is contentdm's abbr for 'file name'
                if not os.path.isfile('{}/{}.{}'.format(alias_dir, pointer, filetype)):
                    binary = p.retrieve_binaries(alias, pointer, "_")
                    p.write_binary_to_file(binary, alias, pointer, filetype)
                    print('wrote', alias, pointer, filetype)



        else:
            print('{} {}, not pointer filetype'.format(pointer, filetype))

    if 'Cpd' in os.listdir(alias_dir):
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
                    orig_filename = simple_etree.find('find').text
                    simple_filetype = os.path.splitext(orig_filename)[-1].replace('.', '')
                    if not os.path.isfile('{}/Cpd/{}/{}.{}'.format(alias_dir, cpd_pointer, simple_pointer, simple_filetype)):
                        binary = p.retrieve_binaries(alias, simple_pointer, "arbitary")
                        simple_filepath = 'Cpd/{}/{}'.format(cpd_pointer, simple_pointer)
                        p.write_binary_to_file(binary, alias, simple_filepath, simple_filetype)
                        print('wrote', alias, cpd_pointer, simple_pointer, simple_filetype)

if __name__ == '__main__':
    get_everything('p16313coll28', ('3632', 'jpg'))