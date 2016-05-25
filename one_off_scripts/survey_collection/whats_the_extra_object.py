#! /usr/bin/env python3

import os
import lxml.etree as ET 

os.chdir('..')


def make_alias_list():
    alias_list = []
    with open('{}/Collections/Collections_List.xml'.format(os.getcwd()), 'r') as f:
        f_read = bytes(bytearray(f.read(), encoding='utf-8'))
        f_etree = ET.fromstring(f_read)
    for item in f_etree.xpath('.//collection'):
        for subitem in item.iter():
            if subitem.tag == 'alias':
                alias_list.append(subitem.text.replace('/', '').strip())
    return alias_list




def introspect_tags():
    obj_list = []
    for alias in make_alias_list():
        file_set = set()
        print(alias)
        for filename in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
            file_set.add(filename)
        for filename in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
            if 'Elems_in_Collection' in filename:
                with open('{}/Collections/{}/{}'.format(os.getcwd(), alias, filename), 'r') as f:
                    f_read = bytes(bytearray(f.read(), encoding='utf-8'))
                    f_etree = ET.fromstring(f_read)
                for obj in f_etree.iter():
                    if obj.tag == 'record':
                        pointer, dmrecord, filetype = None, None, None
                        for sub_obj in obj.getchildren():
                            if sub_obj.tag == 'pointer':
                                pointer = sub_obj.text
                                # if '{}.xml'.format(pointer) not in os.listdir('{}/Collections/{}'.format(os.getcwd(), alias)):
                                #     print(pointer, 'not in directory', alias)
                            # if sub_obj.tag == 'dmrecord':
                            #     dmrecord = sub_obj.text
                            # if sub_obj.tag == 'filetype':
                            #     filetype = sub_obj.text
                                print(alias, pointer)
                                known_faults = {
                                    'ACC': ('174', '175', '176', '177', '178'),
                                    'p16313coll51': ('29383'),
                                    'p16313coll7': ('890', '1145', '1529', '1274'),
                                    }
                                if known_faults.get(alias) and pointer in known_faults[alias]:
                                    continue
                                file_set.remove('{}.xml'.format(pointer))
                        # if pointer and dmrecord and filename:
                        #     obj_list.append((alias, pointer, dmrecord, filetype))
                        # else:
                        #     for variable in [alias, pointer, dmrecord, filetype]:
                        #         if variable:
                        #             print(variable)
                        #             pass
        print([i for i in file_set if i[:-4].isnumeric()])


if __name__ == '__main__':
    introspect_tags()
