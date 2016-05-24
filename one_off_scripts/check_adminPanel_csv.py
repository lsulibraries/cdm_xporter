#! /usr/bin/env python3

import os
import csv


def check_csvs_for_corruption(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        print(filename)
        try:
            csv_reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        except:
            print(filename, "can't be read as a csv")
        headers = next(csv_reader)
        try:
            pointer_col_num = headers.index('CONTENTdm number')
        except:
            print(filename, "doesn't seem to have column for aliases")

        for num, row in enumerate(csv_reader):
            pointer = row[pointer_col_num]
            if not pointer.isnumeric() or (len(pointer) == 0):
                print(pointer, "doesn't seem like a proper pointer")

if __name__ == '__main__':
    csv_dir = '/home/james/Desktop/txtExportfromCDM'
    for file in os.listdir(csv_dir):
        if os.path.isfile(os.path.join(csv_dir, file)):
            fullpath = os.path.join(csv_dir, file)
            check_csvs_for_corruption(fullpath)
