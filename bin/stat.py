#!/usr/bin/env python3

import json
import sys
import os
import ground_truths as gt

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BENCHMARK_DIR = os.path.join(PROJECT_HOME, 'bug-bench/benchmark')

signature_programs = [
    'autotrace-20200219.65',
    'gimp-2.6.7',
    'libxcursor-1.1.14',
    'shntool-3.0.5',
    'sam2p-0.49.4',
    'optipng-0.5.3',
    'latex2rtf-2.1.1',
    'urjtag-0.8',
    'mp3rename-0.6',
    'librelp-1.2.14',
    'zsh-5.4.2',
    'firejail-0.9.62',
    'picocom-2.0a',
    'amanda-3.3.1',
    'schismtracker-20190722',
    'gdk-pixbuf-2.36.11',
    'gocr-0.40',
]


class Alarm:

    def __init__(self, program, src, sink, max_score, min_score, truth):
        self.program = program
        self.src = src
        self.sink = sink
        self.max_score = max_score
        self.min_score = min_score
        self.truth = truth

    def join(self, other):
        src = self.src | other.src
        max_score = max(self.max_score, other.max_score)
        min_score = min(self.min_score, other.min_score)
        truth = self.truth or other.truth
        return Alarm(self.program, src, self.sink, max_score, min_score, truth)

    def insert(self, alarm_lst):
        for a in alarm_lst:
            if (self.program == a.program) and (self.sink == a.sink):
                alarm_lst.remove(a)
                alarm_lst.append(self.join(a))
                return

        alarm_lst.append(self)


# simplify the following two functions
def get_ground_truths(program, target_alarm):
    if program in signature_programs:  # get label from bug-bench
        split_pos = program.rfind('-')
        pname, version = program[:split_pos], program[split_pos + 1:]
        label_json_file = '{}/{}/{}/label.json'.format(BENCHMARK_DIR, pname,
                                                       version)
        with open(label_json_file, 'r') as fp:
            label_json = json.load(fp)
        for label in label_json:
            # infer may print arbitrary subdir names
            if os.path.basename(target_alarm['src']['file']) == os.path.basename(label['source']['file']) and \
                    target_alarm['src']['line'] == label['source']['line'] and \
                    os.path.basename(target_alarm['sink']['file']) == os.path.basename(label['sink']['file']) and \
                    target_alarm['sink']['line'] == label['sink']['line']:
                return True
        return False
    elif program in gt.ground_truths:
        if True in gt.ground_truths[program]:  # get label from groun_truth.py
            for alarm in gt.ground_truths[program][True]:
                if target_alarm['src']['file'] == alarm['src'][
                        'file'] and target_alarm['sink']['line'] == alarm[
                            'sink']['line']:
                    return True
        if False in gt.ground_truths[program]:  # get label from groun_truth.py
            for alarm in gt.ground_truths[program][False]:
                if target_alarm['src']['file'] == alarm['src'][
                        'file'] and target_alarm['sink']['line'] == alarm[
                            'sink']['line']:
                    return False
        return None
    else:
        None


def get_num_bugs(program):
    if program in signature_programs:  # get label from bug-bench
        #TODO: add feature for removing duplicate sinks
        split_pos = program.rfind('-')
        pname, version = program[:split_pos], program[split_pos + 1:]
        label_json_file = '{}/{}/{}/label.json'.format(BENCHMARK_DIR, pname,
                                                       version)
        with open(label_json_file, 'r') as fp:
            label_json = json.load(fp)
        return len(label_json)
    elif program in gt.ground_truths and True in gt.ground_truths[
            program]:  # get label from groun_truth.py

        true_alarms = gt.ground_truths[program][True]

        no_dup_sink = set()
        for true_alarm in true_alarms:
            sink = f'{true_alarm["sink"]["file"]}:{true_alarm["sink"]["line"]}'
            no_dup_sink.add(sink)

        return len(no_dup_sink)
    else:
        return "??"


def get_root_cause_num(all_alarms):
    root_causes = {}
    for alarm in all_alarms:
        if not alarm.truth:
            continue

        program = alarm.program
        src = alarm.src
        score = alarm.max_score
        if program not in root_causes:
            root_causes[program] = [(src, score)]
        else:
            found = False
            for target_src, target_score in root_causes[program]:
                if src & target_src:
                    root_causes[program].remove((target_src, target_score))
                    root_causes[program].append(
                        (src | target_src, max(score, target_score)))
                    found = True
                    break
            if not found:
                root_causes[program].append((src, score))

    over_95 = 0
    over_90 = 0
    over_85 = 0
    over_0 = 0
    for _, rcs in root_causes.items():
        for rc in rcs:
            score = rc[1]
            over_0 += 1
            if score >= 0.85:
                over_85 += 1
            if score >= 0.90:
                over_90 += 1
            if score >= 0.95:
                over_95 += 1
    print(f'95 : {over_95}')
    print(f'90 : {over_90}')
    print(f'85 : {over_85}')
    print(f'0 : {over_0}')


def generate(tracer_out):
    stat = {}
    complete_alarms = []
    for report_file in [
            r for r in os.listdir(tracer_out)
            if r.endswith('json') and r != 'analyze_time.json'
    ]:
        print('Scanning {}'.format(report_file))
        with open('{}/{}'.format(tracer_out, report_file)) as f:
            report = json.load(f)
        under_85 = {True: [], False: []}
        over_85 = {True: [], False: []}
        over_90 = {True: [], False: []}
        over_95 = {True: [], False: []}
        all_alarms = []
        no_trace = 0

        for alarm in report:
            if alarm['weighted_traces'] == []:
                no_trace += 1
            else:
                top_ranked_trace = alarm['weighted_traces'][0]
                first_elem = top_ranked_trace['trace'][0]
                last_elem = top_ranked_trace['trace'][-1]

                target_alarm = {
                    'src': {
                        'file': first_elem['file'],
                        'line': first_elem['line']
                    },
                    'sink': {
                        'file': last_elem['file'],
                        'line': last_elem['line']
                    }
                }

                program = alarm['program']
                src = f"{first_elem['file']}:{first_elem['line']}"
                sink = f"{last_elem['file']}:{last_elem['line']}"
                score = top_ranked_trace['score']
                truth = get_ground_truths(program, target_alarm)
                truth = False if truth == None else truth

                a = Alarm(program, set([src]), sink, score, score, truth)
                a.insert(all_alarms)
                a.insert(complete_alarms)

        for alarm in all_alarms:
            score = alarm.max_score
            truth = alarm.truth
            if score >= 0.95:
                over_95[truth].append(alarm)
                over_90[truth].append(alarm)
                over_85[truth].append(alarm)
            elif score >= 0.90:
                over_90[truth].append(alarm)
                over_85[truth].append(alarm)
            elif score >= 0.85:
                over_85[truth].append(alarm)
            else:
                under_85[truth].append(alarm)
        stat[os.path.splitext(report_file)[0]] = {
            'all_report': report,
            'under_85': under_85,
            'over_85': over_85,
            'over_90': over_90,
            'over_95': over_95,
            'no_trace': no_trace
        }

    get_root_cause_num(complete_alarms)
    return stat


def print_stat(stat):
    print(
        '{0: <20}\t{1: >10}\t{2: >10}\t{3: >10}\t{4: >10}\t{5: >10}\t{6: >10}\t{7: >10}\t{8: >10}\t{9: >10}\t{10: >10}'
        .format('Program', 'Bugs', 'Alarms', 'under_85-True', 'under_85-False',
                'over_85-True', 'over_85-False', 'over_90-True',
                'over_90-False', 'over_95-True', 'over_95-False'))

    total_num_bugs = 0
    total_num_alarms = 0
    under_85 = {True: 0, False: 0}
    over_85 = {True: 0, False: 0}
    over_90 = {True: 0, False: 0}
    over_95 = {True: 0, False: 0}

    for program, report in stat.items():
        # ignore alarms that have empty trace
        num_alarms = len(report['all_report'])
        num_bugs = get_num_bugs(program)
        total_num_bugs += (0 if num_bugs == "??" else num_bugs)
        total_num_alarms += num_alarms
        under_85[True] += len(report['under_85'][True])
        under_85[False] += len(report['under_85'][False]) + report['no_trace']
        over_85[True] += len(report['over_85'][True])
        over_85[False] += len(report['over_85'][False])
        over_90[True] += len(report['over_90'][True])
        over_90[False] += len(report['over_90'][False])
        over_95[True] += len(report['over_95'][True])
        over_95[False] += len(report['over_95'][False])

        print(
            '{0: <20}\t{1: >10}\t{2: >10}\t{3: >10}\t{4: >10}\t{5: >10}\t{6: >10}\t{7: >10}\t{8: >10}\t{9: >10}\t{10: >10}'
            .format(
                program, num_bugs, num_alarms, len(report['under_85'][True]),
                len(report['under_85'][False]), len(report['over_85'][True]),
                len(report['over_85'][False]), len(report['over_90'][True]),
                len(report['over_90'][False]), len(report['over_95'][True]),
                len(report['over_95'][False])))

    print(
        '{0: <20}\t{1: >10}\t{2: >10}\t{3: >10}\t{4: >10}\t{5: >10}\t{6: >10}\t{7: >10}\t{8: >10}\t{9: >10}\t{10: >10}'
        .format("Total", total_num_bugs, total_num_alarms, under_85[True],
                under_85[False], over_85[True], over_85[False], over_90[True],
                over_90[False], over_95[True], over_95[False]))


if __name__ == '__main__':
    stat = generate(sys.argv[1])
    print_stat(stat)
