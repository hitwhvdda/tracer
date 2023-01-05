from typing import List

from paths import PROJECT_HOME, JULIET_TESTCASE_DIR, INFER_BIN, RESULT_DIR, GLOBAL_RESULT_DIR

import csv
import datetime
import os
import subprocess
import time
import typer


def is_cwe_exist(cwe_number):
    prefix = f'CWE{cwe_number}_'
    for d in os.listdir(JULIET_TESTCASE_DIR):
        if d.startswith(prefix):
            return d
    return None


def run_infer(file_path, filename_head, filename_num, extension):
    num_cores = 20
    testcasesupport_dir = os.path.join(PROJECT_HOME, 'juliet-test-suite-c',
                                       'testcasesupport')
    io_c = os.path.join(testcasesupport_dir, 'io.c')

    file_path_prefix_pos = file_path.rfind('/')
    file_path_prefix = file_path[:file_path_prefix_pos]
    target_file = os.path.join(file_path_prefix,
                               f'{filename_head}_{filename_num}*.{extension}')
    link_flag = '-lc++abi -lstdc++ -lm'

    compile_cmd = f'clang -I {testcasesupport_dir} -D INCLUDEMAIN -D OMITGOOD {io_c} {target_file} {link_flag}'

    return subprocess.check_output(
        f'{INFER_BIN} run --juliet --api-misuse-only -j {num_cores} -- {compile_cmd}',
        shell=True)


def run_infer_all(cwe_dir, result_dir):
    result_map = {'issue': 0, 'no_issue': 0, 'error': 0}
    no_issue_files = []

    start_time = time.time()

    target_dir = os.path.join(JULIET_TESTCASE_DIR, cwe_dir)
    for file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file)
        if os.path.isdir(file_path):
            subdir_result = run_infer_all(file_path, result_dir)
            result_map['issue'] += subdir_result['issue']
            result_map['no_issue'] += subdir_result['no_issue']
            result_map['error'] += subdir_result['error']
            no_issue_files += subdir_result['no_issue_files']
            continue

        if '.' not in file or 'CWE' not in file:
            continue

        # windows-specific testcases
        if 'w32' in file or 'wchar_t' in file:
            continue

        filename, extension = file.split('.')
        if not (extension == 'c' or extension == 'cpp'):
            continue

        split_pos = filename.rfind('_')
        filename_head = filename[:split_pos]
        cwe_num = filename_head[0:filename_head.find('_')]
        filename_suffix = filename[split_pos + 1:]

        try:
            if filename_suffix[-1].isalpha():
                if filename_suffix[-1] != 'a':
                    continue
                filename_num = filename_suffix[:-1]
            else:
                filename_num = filename_suffix

            result_path = os.path.join(
                result_dir, f'{cwe_num}_{filename_num}-{filename_head}')
            os.mkdir(result_path)
            os.chdir(result_path)
            result = run_infer(file_path, filename_head, filename_num,
                               extension)
            os.chdir(result_dir)

            if b'No issues found' in result:
                no_issue_files.append(file_path)
                result_map['no_issue'] += 1
            else:
                result_map['issue'] += 1

        except subprocess.CalledProcessError:
            result_map['error'] += 1

    result_map['time'] = time.time() - start_time
    result_map['no_issue_files'] = no_issue_files

    return result_map


def generate_result_csv(result_map, result_dir):
    csv_path = os.path.join(result_dir, 'result.csv')
    with open(csv_path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            'CWE NUMBER', 'ALL_TESTCASES', 'TIME(s)', 'ISSUE', 'NO ISSUE',
            'ERROR'
        ])

        for cwe_number in result_map:
            cwe_number_info = result_map[cwe_number]

            time = cwe_number_info['time']
            issue = cwe_number_info['issue']
            no_issue = cwe_number_info['no_issue']
            error = cwe_number_info['error']
            all = issue + no_issue + error

            writer.writerow([cwe_number, all, time, issue, no_issue, error])


def generate_no_issue_files(result_map, result_dir):
    txt_path = os.path.join(result_dir, 'no_issue_files.txt')
    with open(txt_path, 'w') as f:
        for cwe_number in result_map:
            no_issue_files = result_map[cwe_number]['no_issue_files']

            for file in no_issue_files:
                f.write(file)
                f.write('\n')


def main(cwes: List[int],
         generate_csv: bool = typer.Option(False),
         global_result: bool = typer.Option(False)):

    result_dir = GLOBAL_RESULT_DIR if global_result else RESULT_DIR
    timestamp = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    juliet_result_dir = os.path.join(result_dir, f'juliet-result-{timestamp}')
    os.mkdir(juliet_result_dir)

    result_map = {}
    for cwe_number in cwes:
        if (result := is_cwe_exist(cwe_number)) == None:
            pass
        else:
            result_map[cwe_number] = run_infer_all(result, juliet_result_dir)

    if generate_csv:
        generate_result_csv(result_map, juliet_result_dir)

    generate_no_issue_files(result_map, juliet_result_dir)


if __name__ == '__main__':
    typer.run(main)