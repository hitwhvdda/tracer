#!/usr/bin/env python3
from paths import PROJECT_HOME, GLOBAL_RESULT_DIR

import datetime
import json
import os
import shutil
import subprocess
import typer

NOW_DATETIME = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')


def initialize(result_dir):
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)


def analyze(package, timeout, result_dir, result_dict):
    # init result dict value
    if package not in result_dict:
        result_dict[package] = {}

    # execute run-vuddy-debian.sh for each package
    run_vuddy_script = os.path.join(PROJECT_HOME, 'bin/run-vuddy-debian.sh')

    try:
        subprocess.call([
            run_vuddy_script, '-p', package, '-o', result_dir, '-v',
            os.path.join(PROJECT_HOME, 'result', 'hashmark_4_vuln-bench.hidx')
        ])
    except subprocess.TimeoutExpired:
        output_dir = os.path.join(result_dir, package)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        return


def main(start: int, end: int, timeout: int):
    result_dir = os.path.join(GLOBAL_RESULT_DIR,
                              f'vuddy-debian-{NOW_DATETIME}')
    initialize(result_dir)

    result_dict = {}

    # get popcon package list by 'https://popcon.debian.org/stable/by_inst'
    popcon_install_list_path = os.path.join(
        PROJECT_HOME, 'result/popcon-install-list-clean.txt')

    with open(popcon_install_list_path, 'r') as f:
        popcon_packages = f.readlines()

    popcon_packages = [s.split(',')[3].strip() for s in popcon_packages]

    # run analysis
    while start < end:
        if start >= len(popcon_packages):
            break

        package = popcon_packages[start]
        analyze(package, timeout, result_dir, result_dict)

        start += 1


if __name__ == '__main__':
    typer.run(main)
