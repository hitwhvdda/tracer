#!/usr/bin/env python3

# description: run vuddy using our own signature
# requirements:
#     - hashmark_4_vulnDB-trace-nodes.hidx
#     - hidx files to analyze corresponding to the packages listed in result/selected-packages.txt

import os
import json
import shutil

USAGE = "python3 run-vuddy.py"
PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BENCH_LIST = os.path.join(PROJECT_HOME, 'result/selected-packages.txt')
HIDX_DIR = os.path.join(PROJECT_HOME, 'hmark-4.1.0/hidx')
VULN_HIDX = os.path.join(HIDX_DIR, 'hashmark_4_vulnDB-trace-nodes.hidx')
OUT_DIR = os.path.join(PROJECT_HOME, 'result/vuddy-selected-sig')
LOG_FILE = os.path.join(OUT_DIR, 'log')


def parse_hidx(filename):
    hidx = open(filename, 'r')
    metadata = hidx.readline()
    fingerprints = hidx.read()
    fingerprints = fingerprints.replace("'", '"')
    fingerprints = json.loads(fingerprints)
    hidx.close()
    return fingerprints


def query(vul_fps, tgt_fp, tgt_pgm):
    length = tgt_fp['function length']
    hash = tgt_fp['hash value']
    ret = []
    for vul_fp in vul_fps:
        if vul_fp['function length'] == length and vul_fp['hash value'] == hash:
            pair = {}
            pair['tgt program'] = tgt_pgm
            pair['tgt file'] = tgt_fp['file']
            pair['tgt function id'] = tgt_fp['function id']
            pair['vul file'] = vul_fp['file']
            pair['vul function id'] = vul_fp['function id']
            pair['hash value'] = hash
            ret.append(pair)
    return ret


def run_all_bench():
    if os.path.exists(OUT_DIR) and os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    vul_fps = parse_hidx(VULN_HIDX)
    with open(BENCH_LIST, "r") as fp:
        bench_list = fp.read().splitlines()
    open(LOG_FILE, 'w').close()
    log_file = open(LOG_FILE, 'a')
    for bench in bench_list:
        TARGET_HIDX = os.path.join(HIDX_DIR, 'hashmark_4_' + bench + '.hidx')
        if os.path.isfile(TARGET_HIDX):
            print('analyzing', TARGET_HIDX, '...')
            tgt_fps = parse_hidx(TARGET_HIDX)
            alarms = []
            for tgt_fp in tgt_fps:
                alarms += query(vul_fps, tgt_fp, bench)
            log_file.write('SUCCESS: (' + bench + ') found ' +
                           str(len(alarms)) + ' vulnerable pairs from ' +
                           TARGET_HIDX + '\n')
            with open(os.path.join(OUT_DIR, bench + '.json'),
                      'w') as result_json:
                json.dump(alarms, result_json)
        else:
            log_file.write('ERROR: (' + bench + ') cannot find ' +
                           TARGET_HIDX + '\n')
    log_file.close()


run_all_bench()