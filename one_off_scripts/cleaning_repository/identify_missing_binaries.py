#! /usr/bin/env python3

import os
import re
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

not_converted = []


def check(folder):
    for root, dirs, files in os.walk(folder):
        if len(root.split('/')) > 5:
            if root.split('/')[5] in we_dont_migrate:
                print('skipping', root.split('/')[5])
                continue

        numeric_file_regex = re.compile('[0-9]+.xml')
        pointer_xmls = [i for i in files if numeric_file_regex.match(i)]
        for pointer_xml in pointer_xmls:
            pointer = pointer_xml.split('.')[0]
            if "{}_cpd.xml".format(pointer) in files:
                continue    # skip root level of compound objects

            if ('{}.jp2'.format(pointer) in files) or \
               ('{}.pdf'.format(pointer) in files) or \
               ('{}.mp4'.format(pointer) in files) or \
               ('{}.mp3'.format(pointer) in files):
                continue
            else:
                not_converted.append("{}/{}".format(root, pointer_xml))
                print(not_converted[0])

    for i in not_converted:
        print(i)


if __name__ == '__main__':
    try:
        folder = sys.argv[1]
    except IndexError:
        print('\nChange to: "python identify_missing_binaries.py $folder\n')
        quit()
    check(folder)
