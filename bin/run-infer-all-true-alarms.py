#!/usr/bin/env python3
import datetime
import json
import os
import shutil
import subprocess
import urllib.request

from ground_truths import ground_truths

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

NOW_DATETIME = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
RESULT_DIR = os.path.join('/data/pattern/result',
                          f'all-true-alarms-{NOW_DATETIME}')

true_alarm_packages = ground_truths.keys()


def initialize():
    if not os.path.isdir(RESULT_DIR):
        os.mkdir(RESULT_DIR)


def analyze(package, timeout, result_dict):
    # init result dict value
    if package not in result_dict:
        result_dict[package] = {}

    # execute run-infer-debian.sh for each package
    run_infer_script = os.path.join(PROJECT_HOME, 'bin/run-infer-debian.sh')

    try:
        subprocess.call([
            run_infer_script, '-p', package, '-o', RESULT_DIR, '-t',
            str(timeout + 60), '-i',
            '--api-misuse-only -j 20 --api-misuse-max-fp 5 --api-misuse-max-set 10',
            '-d'
        ],
                        timeout=timeout)
    except subprocess.TimeoutExpired:
        output_dir = os.path.join(RESULT_DIR, package)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        return

    # record number of bugs by bug type
    report_json = os.path.join(RESULT_DIR, package, 'infer-out', 'report.json')

    if os.path.isfile(report_json):
        report_f = open(report_json, 'r')

        report = json.load(report_f)

        integer_overflow = 0
        integer_underflow = 0
        format_string = 0
        buffer_overflow = 0
        command_injection = 0
        for elem in report:
            bug_type = elem['qualifier']
            if bug_type == 'IntOverflow.':
                integer_overflow += 1
            elif bug_type == 'IntUnderflow.':
                integer_underflow += 1
            elif bug_type == 'FormatString.':
                format_string += 1
            elif bug_type == 'BufferOverflow.':
                buffer_overflow += 1
            elif bug_type == 'CmdInjection.':
                command_injection += 1

        result_dict[package]['integer_overflow'] = integer_overflow
        result_dict[package]['integer_underflow'] = integer_underflow
        result_dict[package]['format_string'] = format_string
        result_dict[package]['buffer_overflow'] = buffer_overflow
        result_dict[package]['command_injection'] = command_injection

        report_f.close()


if __name__ == '__main__':
    initialize()
    result_dict = {}
    timeout = 1200

    # run analysis
    for package in true_alarm_packages:
        analyze(package, timeout, result_dict)

    # write anlysis result to result/true-alarms-result.json
    result_json = os.path.join(RESULT_DIR, 'true-alarms-result.json')
    with open(result_json, 'w') as result_f:
        json.dump(result_dict, result_f)