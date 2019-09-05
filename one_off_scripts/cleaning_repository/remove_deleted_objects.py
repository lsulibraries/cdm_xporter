#!/usr/bin/env python3

import os
import lxml.etree as etree
import sys

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
                   'p16313coll18', 'p15140coll33', 'LST', 'MPF', 'LOYOLA_ETDa', 'LOYOLA_ETDb', }


def scan(root_dir):
    repo_extra_files = []
    for folder in (i for i in os.listdir(root_dir) if os.path.isdir("{}/{}".format(root_dir, i))):
        if folder in we_dont_migrate:
            print('skipping', folder)
            continue

        subdir = "{}/{}".format(root_dir, folder)
        collection_pointers = set()
        for Elems_file in (i for i in os.listdir(subdir) if ("Elems_in_Collection" in i) and (".xml" in i)):
            elems_file_etree = etree.parse("{}/{}".format(subdir, Elems_file))
            for pointer in elems_file_etree.findall(".//pointer"):
                collection_pointers.add(pointer.text)

        extra_files = set()
        for file in os.listdir(subdir):
            if (file.split('.')[0] not in collection_pointers) and (file.split('_')[0] not in collection_pointers):
                if ('Elems' in file) or ('Collection' in file) or ('Cpd' in file) or ('Thumbs' in file):
                    continue
                extra_files.add(file.split('.')[0].split('_')[0])

        if extra_files:
            repo_extra_files.append((folder, extra_files))

    print('repo extra files:', repo_extra_files)


if __name__ == '__main__':
    try:
        folder = sys.argv[1]
    except IndexError:
        print('\nChange to: "remove_deleted_objects.py $folder\n\n')
        quit()
    scan(folder)
