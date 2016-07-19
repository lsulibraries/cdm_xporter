#! /usr/bin/env/ python3

import os


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

not_converted_yet = []

for root, dirs, files in os.walk('/media/garrett_armstrong/U/Cached_Cdm_files'):
    if len(root.split('/')) > 5:
        if root.split('/')[5] in we_dont_migrate:
            print('skipping', root.split('/')[5])
            continue
    lowercase_files = {i.lower() for i in files}
    for file in files:
        if file.split('.')[0].isnumeric():
            orig_ext = file.split('.')[-1]
            if orig_ext in ('json', 'xml', 'jp2', 'mp4', 'pdf', 'mp3'):
                continue

            if "{}.jp2".format(file.split('.')[0]) in lowercase_files:
                new_ext = "jp2"
            elif "{}.mp4".format(file.split('.')[0]) in lowercase_files:
                new_ext = "mp4"
            elif "{}.pdf".format(file.split('.')[0]) in lowercase_files:
                new_ext = "pdf"
            elif "{}.mp3".format(file.split('.')[0]) in lowercase_files:
                new_ext = "mp3"
            else:
                not_converted_yet.append((root, file))
                continue

            # new_text = ''
            # xmlpath = "{}.xml".format(os.path.join(root, file.split('.')[0]))
            # print(xmlpath)
            # with open(xmlpath, 'r') as f:
            #     for line in f.readlines():
            #         if orig_ext in line:
            #             line = line.replace(orig_ext, new_ext)
            #         new_text += line
            #     print(new_text)
            #     print(file, orig_ext, new_ext)
            # uncomment if you want to overwrite files -->
            # with open(xmlpath, 'w') as f:
            #     f.write(new_text)

print(not_converted_yet)