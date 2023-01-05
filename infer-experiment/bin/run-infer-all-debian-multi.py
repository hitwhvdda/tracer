#!/usr/bin/env python3
from paths import PROJECT_HOME, GLOBAL_RESULT_DIR, RESULT_DIR
from typing import Optional, List

import datetime
import json
import os
import shutil
import subprocess
import time
import typer

NOW_DATETIME = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')


def initialize(result_dir):
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)


def analyze(package, timeout, use_docker, result_dir, result_dict):
    # init result dict value
    if package not in result_dict:
        result_dict[package] = {}

    # execute run-infer-debian.sh for each package
    run_infer_script = os.path.join(PROJECT_HOME, 'bin/run-infer-debian.sh')
    docker_option = "-d" if use_docker else ""

    start_time = time.time()
    subprocess.call(
        [
            run_infer_script, '-p', package, '-o', result_dir, '-t',
            str(timeout + 60), '-i',
            '--api-misuse-only -j 20 -q --api-misuse-max-fp 5 --api-misuse-max-set 10',
            docker_option
        ],
        timeout=timeout,
    )
    analyze_time = time.time() - start_time

    # record number of bugs by bug type
    report_json = os.path.join(result_dir, package, 'infer-out', 'report.json')

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
        result_dict[package]['analyze_time'] = analyze_time

        report_f.close()


def extract_section(full_section):
    if '/' in full_section:
        slash_pos = full_section.rfind('/')
        return full_section[slash_pos + 1:]
    else:
        return full_section[9:]


def get_packages_by_section(sections):
    debian_packages_by_section_json = os.path.join(
        RESULT_DIR, 'debian-list-by-sections.json')
    with open(debian_packages_by_section_json, 'r') as f:
        debian_packages_by_section = json.load(f)

    if sections:
        selected_sections = sections
    else:
        selected_sections_txt = os.path.join(RESULT_DIR,
                                             'selected-sections.txt')
        with open(selected_sections_txt, 'r') as f:
            selected_sections = [line.strip() for line in f.readlines()]

    popcon_packages = []

    for key, val in debian_packages_by_section.items():
        for section in selected_sections:
            if extract_section(key) == section:
                popcon_packages += val
                break

    return popcon_packages


def get_packges_by_selected():
    selected_packages = os.path.join(RESULT_DIR, 'selected-packages.txt')
    with open(selected_packages, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def main(start: int,
         end: int,
         timeout: int,
         use_docker: bool,
         sections: Optional[List[str]] = typer.Option(None)):
    result_dir = os.path.join(GLOBAL_RESULT_DIR,
                              f'all-debian-multi-{NOW_DATETIME}')
    initialize(result_dir)

    result_dict = {'start': start, 'end': end}

    popcon_packages = get_packges_by_selected()

    timeout_packages = 0

    # run analysis
    while start < end:
        if start >= len(popcon_packages):
            break

        package = popcon_packages[start]
        try:
            analyze(package, timeout, use_docker, result_dir, result_dict)
        except subprocess.TimeoutExpired:
            output_dir = os.path.join(result_dir, package)
            if os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
            timeout_packages += 1

        start += 1

    result_dict['timeout_packages'] = timeout_packages

    # write anlysis result to result/debian-result.json
    result_json = os.path.join(result_dir, 'debian-result.json')
    with open(result_json, 'w') as result_f:
        json.dump(result_dict, result_f)


if __name__ == '__main__':
    typer.run(main)
