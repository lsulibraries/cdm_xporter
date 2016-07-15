#! /usr/bin/env python3

import os
import csv

with open('output_name_items.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter='\t')
    pids_migrate = set()
    for row in csvreader:
        pids_migrate.add(row[0])

print(pids_migrate)
