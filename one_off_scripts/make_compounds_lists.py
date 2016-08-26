#! /usr/bin/env python3

import os
import lxml.etree as etree


starting_dir = '../Cached_Cdm_files'


def identify_simpl_compound_pointers(root, files):
    simple_pointers = []
    compound_pointers = []
    elems_files = [i for i in files if ('Elems_in_Collection' in i) and ('.xml' in i)]

    for elems_file in elems_files:
        elems_etree = etree.parse(os.path.join(root, elems_file))
        simples_sublist = [i.text for i in elems_etree.findall('.//pointer')
                           if [j for j in i.itersiblings(tag='find')
                               if 'cpd' not in j.text]]
        compound_sublist = [i.text for i in elems_etree.findall('.//pointer')
                            if [j for j in i.itersiblings(tag='find')
                                if 'cpd' in j.text]]
        for i in simples_sublist:
            simple_pointers.append(i)
        for i in compound_sublist:
            compound_pointers.append(i)

    return(simple_pointers, compound_pointers)


def write_compounds_config_list(root, compound_parents):
    os.makedirs('output', exist_ok=True)
    alias_level = root.split('/').index('Cached_Cdm_files') + 1
    alias = root.split('/')[alias_level]
    print(alias, compound_parents)
    file_text = ''.join("{}\n".format(i) for i in compound_parents)
    with open('output/{}_compounds.txt'.format(alias), 'w') as f:
        f.write(file_text)


if __name__ == '__main__':
    for root, dirs, files in os.walk(starting_dir):
        if root.split('/')[-2] == 'Cached_Cdm_files':
            print(root)
            simple_pointers, compound_parents = identify_simpl_compound_pointers(root, files)
            write_compounds_config_list(root, compound_parents)
