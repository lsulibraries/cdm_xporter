#! /usr/bin/env python3

import os

os.chdir('..')

if 'HiddenPointers' not in os.listdir('{}/Collections/BRS'.format(os.getcwd())):
    os.mkdir('{}/Collections/BRS/HiddenPointers'.format(os.getcwd()))

for filename in os.listdir('{}/Collections/BRS'.format(os.getcwd())):
    if filename not in ('HiddenPointers'):
        if filename not in os.listdir('{}/Collections/BRS_as_reported_by_CDM'.format(os.getcwd())):
            os.rename(
                '{}/Collections/BRS/{}'.format(os.getcwd(), filename),
                '{}/Collections/BRS/HiddenPointers/{}'.format(os.getcwd(), filename)
                )
            print(filename)
