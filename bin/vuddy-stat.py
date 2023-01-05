#!/usr/bin/env python3

from genericpath import isfile
import json
import sys
import os
import csv

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
VUDDY_RESULT = os.path.join(PROJECT_HOME, 'result/vuddy-selected')
BENCH_LIST = os.path.join(PROJECT_HOME, 'result/selected-packages.txt')
RESULT_CSV = os.path.join(VUDDY_RESULT, 'result.csv')

# alarms of our interest
cwe_list = [
    'CWE-78', 'CWE-120', 'CWE-121', 'CWE-122', 'CWE-126', 'CWE-129', 'CWE-134',
    'CWE-190', 'CWE-191', 'CWE-680'
]


def parse_json(filename):
    '''takes program.json and returns the result tuple'''
    ret = []
    with open(filename, "r") as json_file:
        data = json.load(json_file)
    #metadata = data[0]
    #alarms = data[1:-1]
    metadata, *alarms = data
    ret = [metadata["total_vulfunc"]]

    # counts number of alarms corresponding to global cwe_list
    cwe_count = []
    for cwe in cwe_list:
        cnt = 0
        for alarm in alarms:
            if alarm["cwe"] == cwe:
                cnt += 1
        cwe_count.append(cnt)
    ret += cwe_count
    return ret


if __name__ == '__main__':
    with open(BENCH_LIST, "r") as fp:
        bench_list = fp.read().splitlines()

    # generate data for csv
    header = ['program', '#alarms'] + cwe_list
    rows = []
    for bench in bench_list:
        filename = os.path.join(VUDDY_RESULT, bench + '.json')
        row = [bench]
        if (os.path.isfile(filename)):
            row = row + parse_json(filename)
        else:
            row += [0] * (len(header) - 1)
        rows.append(row)

    for row in rows:
        print(row)

    # write csv
    with open(RESULT_CSV, 'w', encoding='UTF8', newline='') as fp:
        writer = csv.writer(fp)

        writer.writerow(header)

        # write multiple rows
        writer.writerows(rows)
