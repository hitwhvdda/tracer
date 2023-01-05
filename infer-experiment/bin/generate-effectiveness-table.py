from ground_truths import ground_truths

import click
import json
import os


class Alarm:
    def __init__(self, program, src, sink, bug_type, score, signature):
        self.program = program
        self.src = src
        self.sink = sink
        self.bug_type = bug_type
        self.score = score
        self.signature = signature

    def join(self, other):
        if self.bug_type != other.bug_type:
            print(self.bug_type, other.bug_type)

        if self.score >= other.score:
            signature = self.signature
        else:
            signature = other.signature

        return Alarm(self.program, self.src, self.sink, self.bug_type,
                     max(self.score, other.score), signature)

    def insert(self, alarm_lst):
        for alarm in alarm_lst:
            if self.program == alarm.program and self.sink == alarm.sink:
                alarm_lst.remove(alarm)
                alarm_lst.append(self.join(alarm))
                return

        alarm_lst.append(self)


def equal_line_alarm(line, alarm):
    ((src_file, src_line), (sink_file, sink_line), _, _) = line
    return src_file == alarm['src']['file'] and src_line == alarm['src'][
        'line'] and sink_file == alarm['sink']['file'] and sink_line == alarm[
            'sink']['line']


def parse_line(line):
    def get_elem(s):
        start_ind = line.find(s) + len(s)
        if (comma_ind := line.find(',', start_ind)) < 0:
            end_ind = len(line)
        else:
            end_ind = comma_ind
        return line[start_ind:end_ind]

    src_file, src_line = get_elem('src: ').split(':')
    src_line = int(src_line)
    sink_file, sink_line = get_elem('sink: ').split(':')
    sink_line = int(sink_line)
    score = float(get_elem('score: '))
    bug_type = get_elem('bug_type: ').strip()

    return ((src_file, src_line), (sink_file, sink_line), score, bug_type)


def get_signature(line, result_json):
    ((src_file, src_line), (sink_file, sink_line), _, _) = line
    with open(result_json, 'r') as f:
        result = json.load(f)
        for alarm in result:
            weighted_trace = alarm['weighted_traces'][0]
            trace = weighted_trace['trace']
            if trace[0]['file'] == src_file and alarm[
                    'src'] == src_line and trace[-1][
                        'file'] == sink_file and alarm['sink'] == sink_line:
                return weighted_trace['signature']


def find_alarm_info(alarm, program, tracer_result):
    bug_type_map = {
        '"IntOverflow."': 'Integer Overflow',
        '"IntUnderflow."': 'Integer Underflow',
        '"BufferOverflow."': 'Buffer Overflow',
        '"FormatString."': 'Format String',
        '"CmdInjection."': 'Command Injection'
    }

    result_txt = os.path.join(tracer_result, f'{program}.txt')
    with open(result_txt, 'r') as f:
        for line in f.readlines():
            line_info = parse_line(line)
            if equal_line_alarm(line_info, alarm):
                ((src_file, src_line), (sink_file, sink_line), score,
                 bug_type) = line_info
                bug_type = bug_type_map[bug_type]

                result_json = os.path.join(tracer_result, f'{program}.json')
                signature = get_signature(line_info, result_json)
                return Alarm(program, f'{src_file}:{src_line}',
                             f'{sink_file}:{sink_line}', bug_type,
                             float(score), signature)


def repr_sig(signature):
    if signature.startswith('CWE'):
        head_ind = signature.find('_')
        return f'Juliet-{signature[:head_ind]}'

    signature_map = {
        'buffer-overflow1': 'OWASP tutorial',
        'command-injection1': 'OWASP tutorial',
        'command-injection2': 'OWASP tutorial',
        'command-injection3': 'OWASP tutorial',
        'command-injection4': 'OWASP tutorial',
        'shntool-3.0.5': 'shntool-3.0.5~\\cite{Heo2017}',
        'mp3rename-0.6': 'mp3rename-0.6~\\cite{Heo2017}',
        'autotrace-20200219.65': 'CVE-2017-9181',
        'sam2p-0.49.4': 'CVE-2017-16663',
        'amanda-3.3.1': 'CVE-2016-10729',
        'latex2rtf-2.1.1': 'CVE-2015-8106',
        'gdk-pixbuf-2.36.11': 'CVE-2017-6313',
        'optipng-0.5.3': 'CVE-2017-1000229',
        'gimp-2.6.7': 'CVE-2009-1570',
        'zsh-5.4.2': 'CVE-2018-1100',
        'picocom-2.0a': 'CVE-2015-9059',
        'schismtracker-20190722': 'CVE-2019-14523',
    }

    head_ind = signature.rfind('-')
    return signature_map[signature[:head_ind]]


@click.command()
@click.argument('tracer-result', type=click.Path(exists=True, file_okay=False))
def main(tracer_result):

    all_alarms = []
    for program in ground_truths.keys():
        try:
            true_alarms = ground_truths[program][True]
        except KeyError:
            continue
        for alarm in true_alarms:

            try:
                a = find_alarm_info(
                    alarm,
                    program,
                    tracer_result,
                )
            except:
                print(alarm)
                continue

            a.insert(all_alarms)

    result = {}
    for alarm in all_alarms:
        program = alarm.program
        if program not in result:
            result[program] = {}

        if alarm.bug_type not in result[program]:
            result[program][alarm.bug_type] = {
                'min_score': alarm.score,
                'max_score': alarm.score,
                'signature': alarm.signature,
                'count': 1
            }
        else:
            elem = result[program][alarm.bug_type]
            elem['count'] += 1
            if elem['min_score'] > alarm.score:
                elem['min_score'] = alarm.score
            if elem['max_score'] < alarm.score:
                elem['max_score'] = alarm.score
                elem['signature'] = alarm.signature

    lines = []
    for program, elem in result.items():
        if elem:
            for bug_type in elem:
                info = elem[bug_type]
                bug_cnt = info['count']
                min_score = '{:0.2f}'.format(info['min_score'])
                max_score = '{:0.2f}'.format(info['max_score'])

                signature = info['signature']

                lines.append((program, bug_cnt, bug_type, min_score, max_score,
                              signature))

    lines.sort(key=lambda x: (x[0], x[2]))

    click.echo(
        '\\textbf{Program}\t&\t\\textbf{Bugs}\t&\t\\textbf{Bug Type}\t&\t\\textbf{Score}\t&\t\\textbf{Signature}\t&\t\\textbf{CVE Assigned}\t\\\\\t\\midrule'
    )
    for program, bug_cnt, bug_type, min_score, max_score, signature in lines:
        if min_score == max_score:
            score_str = max_score
        else:
            score_str = f'{min_score}-{max_score}'
        print('\\textsf{' + program + '}\t&\t' + str(bug_cnt) + '\t&\t' +
              bug_type + '\t&\t' + score_str + '\t&\t' + repr_sig(signature) +
              '\t&')


if __name__ == '__main__':
    main()