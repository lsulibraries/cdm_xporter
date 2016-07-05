#! /usr/bin/env python3

import os
from lxml import etree


owner_pidlongstring = '''tahil: tahil-aaw, tahil-abw, tahil-apc, tahil-hpl, tahil-lpc, tahil-rtp
lsu:, lsu-lsap, lsu-brs, lsu-ibe, lsu-act, lsu-brt, lsu-cff, lsu-clt, lsu-cnp, lsu-cwp, lsu-dyp, lsu-fcc, lsu-gcs, lsu-gfm, lsu-gsc, lsu-hpl, lsu-jja, lsu-lhc, lsu-lnp, lsu-mdp, lsu-mrf, lsu-nmi, lsu-noe, lsu-pvc, lsu-rbc, lsu-rbo, lsu-sce, lsu-tjp, lsu-uap, lsu-wls, lsu-mmf, lsu-msw, lsu-neworleans, lsu-nonnegexposures, lsu-p120701coll12, lsu-p120701coll19, lsu-p120701coll22, lsu-p120701coll23, lsu-p120701coll24, lsu-p15140coll10, lsu-p15140coll12, lsu-p15140coll14, lsu-p15140coll17, lsu-p15140coll18, lsu-p15140coll46, lsu-p15140coll54, lsu-p15140coll56, lsu-p16313coll10, lsu-p16313coll31, lsu-p16313coll34, lsu-p16313coll35, lsu-p16313coll54, lsu-p16313coll56, lsu-p16313coll57, lsu-p16313coll58, lsu-p16313coll69, lsu-p16313coll76, lsu-p16313coll79, lsu-p16313coll8, lsu-p16313coll80, lsu-p16313coll81, lsu-p16313coll85, lsu-p16313coll9, lsu-sartainengravings, lsu-tensas, lsu-thw, lsu-tld, lsu-wri-boy, lsu-lapur, lsu-p15140coll21, lsu-p15140coll35, lsu-p15140coll41, lsu-cwd, lsu-crd, lsu-p16313coll45, lsu-p16313coll77, lsu-p16313coll89, lsu-rjr, lsu-p16313coll51, lsu-p16313coll52
lsm: lsm-cca, lsm-hlm, lsm-jaz, lsm-lct, lsm-loh, lsm-lps, lsm-ccc, lsm-fqa, lsm-koh, lsm-mpc, lsm-nac, lsm-ncc, lsm-osc, lsm-p120701coll18, lsm-p15140coll60, lsm-p16313coll83, lsm-rmc, lsm-rsp, lsm-rtc
ull:, ull-lsa, ull-p16313coll26, ull-sip, ull-p16313coll25,
loyno:, loyno-jsn, loyno-lmnp01, loyno-etd, loyno-p120701coll17, loyno-p120701coll9, loyno-p16313coll20, loyno-p16313coll24,  loyno-p16313coll28, loyno-p16313coll48, loyno-p16313coll5, loyno-p16313coll87, loyno-p16313coll91, loyno-p16313coll93, loyno-p16313coll44, loyno-p120701coll28, loyno-p120701coll27
subr:, subr-hwj, subr-vbc
latech:, latech-cmprt
hnoc: lsu-aww, hnoc-clf, hnoc-p15140coll1, hnoc-p15140coll28, hnoc-p16313coll21, hnoc-p16313coll65, hnoc-p16313coll17
lsm: lsm-jnt, lsm-lst, lsm-fjc, lsm-gfm,
lsuhscs: lsuhscs-gwm, lsuhscs-p15140coll23, lsuhscs-p15140coll44
nicholls: nicholls-mpf, nicholls-p15140coll51
ulm: ulm-p120701coll10, ulm-p15140coll26, ulm-p15140coll27, ulm-p16313coll1, ulm-p16313coll43
lsuhscno: lsuhscno-lsubk01, lsuhscno-ncc, lsuhscno-p120701coll26, lsuhscno-p120701coll17, lsuhscno-p15140coll16, lsuhscno-p15140coll19, lsuhscno-p15140coll49, lsuhscno-p15140coll50, lsuhscno-p15140coll52, lsuhscno-p16313coll19
lsus: lsus-tbp, lsus-nwm, lsus-stc
uno: uno-p120701coll29, uno-fbm, uno-hic, uno-ani, uno-jbf, uno-p120701coll13, uno-p120701coll15, uno-p120701coll25, uno-p120701coll8, uno-p15140coll30, uno-p15140coll31, uno-p15140coll4, uno-p15140coll42, uno-p15140coll7, uno-p16313coll2, uno-p16313coll22, uno-p16313coll23, uno-p16313coll61, uno-p16313coll62, uno-p16313coll72, uno-p16313coll86
mcneese: mcneese-p16313coll74, mcneese-psl
state: state-lhp, state-lwp, state-p267101coll4
nsu: nsu-mpa, nsu-ncc'''

owner_tuplepids = {
    'tahil': (
        'tahil-aaw',
        'tahil-abw',
        'tahil-apc',
        'tahil-hpl',
        'tahil-lpc',
        'tahil-rtp',
        'tahil-bba', ),
    'lsu': (
        'lsu-lsap',
        'lsu-brs',
        'lsu-ibe',
        'lsu-act',
        'lsu-brt',
        'lsu-cff',
        'lsu-clt',
        'lsu-cnp',
        'lsu-cwp',
        'lsu-dyp',
        'lsu-fcc',
        'lsu-gcs',
        'lsu-gfm',
        'lsu-gsc',
        'lsu-hpl',
        'lsu-jja',
        'lsu-lhc',
        'lsu-lmp',
        'lsu-lnp',
        'lsu-mdp',
        'lsu-mrf',
        'lsu-nmi',
        'lsu-noe',
        'lsu-pvc',
        'lsu-rbc',
        'lsu-rbo',
        'lsu-sce',
        'lsu-tjp',
        'lsu-uap',
        'lsu-wls',
        'lsu-mmf',
        'lsu-msw',
        'lsu-neworleans',
        'lsu-nonegexposures',
        'lsu-p120701coll12',
        'lsu-p120701coll19',
        'lsu-p120701coll22',
        'lsu-p120701coll23',
        'lsu-p120701coll24',
        'lsu-p15140coll6',
        'lsu-p15140coll10',
        'lsu-p15140coll12',
        'lsu-p15140coll14',
        'lsu-p15140coll17',
        'lsu-p15140coll18',
        'lsu-p15140coll46',
        'lsu-p15140coll54',
        'lsu-p15140coll56',
        'lsu-p16313coll10',
        'lsu-p16313coll31',
        'lsu-p16313coll34',
        'lsu-p16313coll35',
        'lsu-p16313coll54',
        'lsu-p16313coll56',
        'lsu-p16313coll57',
        'lsu-p16313coll58',
        'lsu-p16313coll69',
        'lsu-p16313coll76',
        'lsu-p16313coll79',
        'lsu-p16313coll8',
        'lsu-p16313coll80',
        'lsu-p16313coll81',
        'lsu-p16313coll85',
        'lsu-p16313coll9',
        'lsu-sartainengravings',
        'lsu-tensas',
        'lsu-thw',
        'lsu-tld',
        'lsu-wri-boy',
        'lsu-lapur',
        'lsu-p15140coll21',
        'lsu-p15140coll35',
        'lsu-p15140coll41',
        'lsu-cwd',
        'lsu-crd',
        'lsu-p16313coll45',
        'lsu-p16313coll77',
        'lsu-p16313coll89',
        'lsu-rjr',
        'lsu-p16313coll51',
        'lsu-p16313coll52', ),
    'lsm': (
        'lsm-cca',
        'lsm-hlm',
        'lsm-jaz',
        'lsm-lct',
        'lsm-loh',
        'lsm-lps',
        'lsm-ccc',
        'lsm-fqa',
        'lsm-koh',
        'lsm-jaz',
        'lsm-mpc',
        'lsm-nac',
        'lsm-ncc',
        'lsm-osc',
        'lsm-p120701coll18',
        'lsm-p15140coll60',
        'lsm-p16313coll83',
        'lsm-rmc',
        'lsm-rsp',
        'lsm-rtc',
        'lsm-jnt',
        'lsm-lst',
        'lsm-fjc',
        'lsm-gfm', ),
    'ull': (
        'ull-acc',
        'ull-lsa',
        'ull-p16313coll26',
        'ull-sip',
        'ull-p16313coll25',
        ),
    'loyno': (
        'loyno-jsn',
        'loyno-lmnp01',
        'loyno-etd',
        'loyno-p120701coll17',
        'loyno-p120701coll9',
        'loyno-p16313coll20',
        'loyno-p16313coll24',
        'loyno-p16313coll28',
        'loyno-p16313coll48',
        'loyno-p16313coll5',
        'loyno-p16313coll87',
        'loyno-p16313coll91',
        'loyno-p16313coll93',
        'loyno-p16313coll96',
        'loyno-p16313coll98',
        'loyno-p16313coll44',
        'loyno-p120701coll28',
        'loyno-p120701coll27', ),
    'subr': (
        'subr-hwj',
        'subr-vbc', ),
    'latech': (
       'latech-cmprt', ),
    'hnoc': (
        'lsu-aww',
        'hnoc-lph'
        'hnoc-clf',
        'hnoc-p15140coll1',
        'hnoc-p15140coll28',
        'hnoc-p16313coll21',
        'hnoc-p16313coll65',
        'hnoc-p16313coll17', ),
    'lsuhscs': (
        'lsuhscs-gwm',
        'lsuhscs-ncc'
        'lsuhscs-p15140coll23',
        'lsuhscs-p15140coll44',
        'lsuhscs-p16313coll3', ),
    'nicholls': (
        'nicholls-mpf',
        'nicholls-p15140coll51', ),
    'ulm': (
        'ulm-p120701coll10',
        'ulm-p15140coll26',
        'ulm-p15140coll27',
        'ulm-p16313coll1',
        'ulm-p16313coll43', ),
    'lsuhscno': (
        'lsuhscno-lsubk01',
        'lsuhscno-ncc',
        'lsuhscno-p120701coll7',
        'lsuhscno-p120701coll26',
        'lsuhscno-p15140coll16',
        'lsuhscno-p15140coll19',
        'lsuhscno-p15140coll49',
        'lsuhscno-p15140coll50',
        'lsuhscno-p15140coll52',
        'lsuhscno-p16313coll19', ),
    'lsus': (
        'lsus-tbp',
        'lsus-nwm',
        'lsus-stc', ),
    'uno': (
        'uno-p120701coll29',
        'uno-fbm',
        'uno-hic',
        'uno-ani',
        'uno-jbf',
        'uno-omsa',
        'uno-p120701coll13',
        'uno-p120701coll15',
        'uno-p120701coll25',
        'uno-p120701coll8',
        'uno-p15140coll30',
        'uno-p15140coll31',
        'uno-p15140coll4',
        'uno-p15140coll42',
        'uno-p15140coll7',
        'uno-p16313coll2',
        'uno-p16313coll22',
        'uno-p16313coll23',
        'uno-p16313coll61',
        'uno-p16313coll62',
        'uno-p16313coll72',
        'uno-p16313coll86', ),
    'mcneese': (
        'mcneese-p16313coll74',
        'mcneese-psl', ),
    'state': (
        'state-lhp',
        'state-lwp',
        'state-p267101coll4', ),
    'nsu': (
        'nsu-mpa',
        'nsu-ncc', ),
    'tulane': (
        'tulane-p16313coll39',
        'tulane-p16313coll16',
        'tulane-p16313coll29',
        'tulane-p15140coll45',
        'tulane-p15140coll47',
        'tulane-p16313coll41',
        'tulane-p15140coll58',
        'tulane-p16313coll75',
        'tulane-p15140coll38',
        'tulane-p16313coll11',
        'tulane-p16313coll37',
        'tulane-p15140coll15',
        'tulane-p16313coll68',
        'tulane-p15140coll34',
        'tulane-p16313coll73',
        'tulane-p16313coll66',
        'tulane-p16313coll64',
        'tulane-p15140coll29',
        'tulane-p16313coll15',
        'tulane-p16313coll27',
        'tulane-p16313coll6',
        'tulane-ama',
        'tulane-p16313coll4',
        'tulane-p16313coll13',
        'tulane-p16313coll14',
        'tulane-p16313coll59',
        'tulane-p16313coll38',
        'tulane-p16313coll46',
        'tulane-p16313coll53',
        'tulane-p15140coll25',
        'tulane-p16313coll33',
        'tulane-p15140coll37',
        'tulane-p15140coll39',
        'tulane-p16313coll42',
        'tulane-p15140coll40',
        'tulane-p15140coll3',
        'tulane-p16313coll30',
        'tulane-p16313coll63',
        ),
    }

filelist = []
aliases_pids = []
for file in os.listdir('.'):
    if ('.py' in file) or (not file.split('.')[0].isnumeric()):
        continue
    print(file)
    file_etree = etree.parse(os.path.join(os.getcwd(), file))



    file_elements = [i for i in file_etree.findall('.//{http://www.loc.gov/mods/v3}identifier')]
    for i in file_elements:
        if i.attrib.get('displayLabel') == 'Collection Code':
            incoming_alias = i.text
            print(incoming_alias)

    file_elements = [i for i in file_etree.findall('.//{http://www.loc.gov/mods/v3}note')]
    for i in file_elements:
        # print(i.keys())
        if i.attrib.get('displayLabel') == 'Institutions':
            print(i.text)

    filelist.append(str(file))
    for tuple_pid in owner_tuplepids.values():
        for pid in tuple_pid:
            if incoming_alias.lower() == pid.split('-')[-1] or incoming_alias.lower().replace('_', '-') == pid:
                aliases_pids.append('{} \t\t {}'.format(incoming_alias, pid))
                # print(file, '{}.{}'.format(pid, file.split('.')[-1]))
                os.rename(file, '{}.{}'.format(pid, file.split('.')[-1]))

# print(len(aliases_pids), len(filelist))


# for line in owner_pidlongstring.split('\n'):
#     for num, i in enumerate(line.split(' ')):
#         if num == 0:
#             print("'{}': (".format(i.strip(',').strip(':')))
#         else:
#             print("'{}',".format(i.strip(',')))
#     print(')')

# print('alias_to_pid_rename = {')
# for i in alias_to_pid:
#     print('{}: {}'.format(i, i.lower())

# for file in os.listdir('.'):
#     os.rename(file, alias_to_pid[file])
