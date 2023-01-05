#!/usr/bin/env python3

from paths import PROJECT_HOME, BENCHMARK_DIR, GLOBAL_RESULT_DIR

import datetime
import json
import math
import os
import subprocess

integer_overflow_bench = {
    'autotrace': '20200219.65',
    'gimp': '2.6.7',
    'libxcursor': '1.1.14',
    'shntool': '3.0.5',
    'sam2p': '0.49.4',
    'optipng': '0.5.3',
    'gocr': '0.40',
}
format_string_bench = {
    'latex2rtf': '2.1.1',
    'urjtag': '0.8',
    'mp3rename': '0.6',
    # 'sdop', 'a2ps',
}
buffer_overflow_bench = {
    'librelp': '1.2.14',
    'unzip': '6.0',
    'zsh': '5.4.2',
    'leptonica': '1.75.2',
    'libming': '0.4.8',
    # 'openjpeg',
}
cmd_injection_bench = {
    'firejail': '0.9.62',
    'picocom': '2.0a',
    'amanda': '3.3.1',
}
integer_underflow_bench = {
    'schismtracker': '20190722',
    'gdk-pixbuf': '2.36.11',
}

target_bench = [
    integer_overflow_bench, format_string_bench, buffer_overflow_bench,
    cmd_injection_bench, integer_underflow_bench
]

infer_default_option = '--api-misuse-only -j 20 --api-misuse-max-fp 5 --api-misuse-max-set 10'

analyze_option = {
    'latex2rtf':
    f'{infer_default_option} --only-files funct1.c --only-files main.c --only-files parser.c',
    'gdk-pixbuf':
    f'{infer_default_option} --only-files gdk-pixbuf/io-icns.c --only-files gdk-pixbuf/gdk-pixbuf-loader.c',
    'urjtag':
    '--api-misuse-only -j 20 --api-misuse-max-fp 20 --api-misuse-max-set 20'
}

bug_type_map = {
    'IntOverflow.': 'integer-overflow',
    'FormatString.': 'format-string',
    'BufferOverflow.': 'buffer-overflow',
    'CmdInjection.': 'command-injection',
    'IntUnderflow.': 'integer-underflow'
}


def initialize(result_dir):
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)


def analyze(result_dir):
    result_dict = {}

    for bug_pattern in target_bench:
        for bench, version in bug_pattern.items():

            if bench not in result_dict:
                result_dict[bench] = {}

            result_dict[bench][version] = {}

            # execute run_infer.sh for each benchmark
            run_infer_script = os.path.join(PROJECT_HOME, 'bin/run-infer.sh')
            infer_option = analyze_option.get(bench, infer_default_option)
            subprocess.call([
                run_infer_script, '-p', bench, '-v', version, '-o', result_dir,
                '-i', infer_option
            ])

            # compare label.json and report.json
            label_json = os.path.join(BENCHMARK_DIR, bench, version,
                                      'label.json')
            report_json = os.path.join(result_dir, f'{bench}-{version}',
                                       'infer-out', 'report.json')

            label_f = open(label_json, 'r')
            report_f = open(report_json, 'r')

            label = json.load(label_f)
            report = json.load(report_f)

            all_bugs = [(
                {
                    'file': os.path.split(elem['source']['file'])[1],
                    'line': elem['source']['line'],
                },
                {
                    'file': os.path.split(elem['sink']['file'])[1],
                    'line': elem['sink']['line'],
                },
                elem['type'],
            ) for elem in label]
            reported_bugs = [(
                {
                    'file':
                    os.path.split(elem['extras']['bug_src_loc']['file'])[1],
                    'line': elem['extras']['bug_src_loc']['lnum']
                },
                {
                    'file': os.path.split(elem['file'])[1],
                    'line': elem['line']
                },
                bug_type_map[elem['qualifier']],
            ) for elem in report]

            all_alarms = len(reported_bugs)
            true_alarms = sum(1 for bug in reported_bugs if bug in all_bugs)
            false_alarms = all_alarms - true_alarms

            result_dict[bench][version]['#_of_bugs'] = len(all_bugs)
            result_dict[bench][version]['true_alarms'] = true_alarms
            result_dict[bench][version]['false_alarms'] = false_alarms

            # calculate trace info
            trace_num = 0
            trace_len = 0
            for bug in report:
                bug_trace = bug['bug_trace']
                trace_num += len(bug_trace)
                trace_len += sum(len(trace_item) for trace_item in bug_trace)

            trace_avg = 0 if all_alarms == 0 else trace_num / all_alarms
            trace_sdev = 0 if all_alarms == 0 else math.sqrt(
                sum((len(bug['bug_trace']) - trace_avg)**2
                    for bug in report) / all_alarms)

            result_dict[bench][version]['trace_num'] = trace_num
            result_dict[bench][version][
                'trace_avg_len'] = trace_len / trace_num if trace_num != 0 else 0
            result_dict[bench][version]['trace_avg'] = trace_avg
            result_dict[bench][version]['trace_sdev'] = trace_sdev

            label_f.close()
            report_f.close()

    # write result.json from result_dict
    result_json = os.path.join(result_dir, 'result.json')
    with open(result_json, 'w') as result_f:
        json.dump(result_dict, result_f)


if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    result_dir = os.path.join(GLOBAL_RESULT_DIR, f'all-bench-{timestamp}')

    initialize(result_dir)
    analyze(result_dir)
