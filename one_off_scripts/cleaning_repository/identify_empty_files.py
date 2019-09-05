#! /usr/bin/env python3

import os
import sys


def scan(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if not os.path.isfile(filepath):
                continue
            if os.path.getsize(filepath) == 0:
                print(filepath)


if __name__ == '__main__':
    try:
        folder = sys.argv[1]
    except IndexError:
        print('\nChange to: "python identify_empty_file.py $folder\n\n')
        quit()
    scan(folder)
