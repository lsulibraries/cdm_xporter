#! /usr/bin/env python3

import csv
import os

os.chdir('..')

def make_cmp_coll_list():
    cpd_coll_list = []
    with open('alias_name_details.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        for row in csv_reader:
            if row[5].isnumeric():
	            if int(row[5]) > 0:
                	cpd_coll_list.append(row[0])
    return cpd_coll_list

if __name__ == '__main__':
    cpd_collections = make_cmp_coll_list()
    print(cpd_collections)

cpd_collections = ['LSM_MPC', 'JSN', 'p120701coll17', 'LMP', 'MSW', 'p120701coll22', 'p15140coll14', 'p15140coll44',
'p16313coll3', 'MPF', 'p15140coll51', 'LHP', 'p15140coll45', 'p16313coll12', 'p16313coll37', 'p16313coll41',
'p16313coll63', 'p120701coll8', 'p15140coll32', 'UNO_JBF', 'p16313coll36', 'CMPRT', 'HLM', 'LSU_RBC', 'wri-boy',
'PSL', 'p16313coll71', 'p16313coll25', 'IBE', 'LSU_BRT', 'LSU_LHC', 'p16313coll19', 'p15140coll34',
'p16313coll26', 'p16313coll72', 'AWW', 'LSM_KOH', 'p16313coll66', 'p120701coll13', 'p120701coll15',
'p16313coll22', 'BBA', 'p120701coll7', 'p15140coll19', 'ABW', 'LSU_NMI', 'p16313coll69', 'LSUS_TBP',
'BTW', 'p120701coll6', 'p15140coll27', 'p15140coll39', 'p120701coll9', 'APC', 'p16313coll59', 'p16313coll64',
'p16313coll83', 'p120701coll24', 'HHN', 'HPL', 'p16313coll30', 'p15140coll26', 'LSU_SCE', 'p16313coll86',
'p16313coll91', 'p16313coll81', 'p16313coll5', 'p15140coll37', 'p15140coll4', 'p120701coll12', 'LPH',
'LSU_GSC', 'p15140coll18', 'p16313coll35', 'p16313coll31', 'p120701coll29', 'p15140coll17', 'LSU_CNP',
'MMF', 'p16313coll57', 'p16313coll1', 'p16313coll14', 'p16313coll44', 'HNF', 'p15140coll6', 'p16313coll68',
'p16313coll80', 'p120701coll28', 'LPC', 'HTU', 'p15140coll42', 'p16313coll93', 'p15140coll40', 'p16313coll65',
'LSU_ACT', 'LSU_NOE', 'p16313coll8', 'p15140coll30', 'p120701coll19', 'LSU_LNP', 'p16313coll9', 'p267101coll4',
'p16313coll32', 'p16313coll76', 'p16313coll34', 'p16313coll43', 'LSU_CFF', 'p16313coll50', 'p15140coll25',
'p16313coll29', 'p15140coll10', 'p15140coll49', 'AAW', 'p15140coll60', 'LSU_CWP', 'LSUBK01', 'UNO_ANI',
'p120701coll26', 'LOYOLA_ETD', 'LSU_MDP', 'LSU_UAP', 'p15140coll41', 'p15140coll31', 'LSUHSC_NCC', 'p15140coll7',
'p16313coll2', 'p15140coll52', 'p15140coll50', 'p16313coll10', 'lapur', 'p16313coll17', 'UNO_SCC', 'LWP',
'p120701coll25', 'p15140coll23', 'p16313coll51', 'LMNP01']
