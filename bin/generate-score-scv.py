from ctypes import ArgumentError
from ground_truths import ground_truths
from paths import RESULT_DIR

import click
import csv
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os


class PlotDrawer:
    def __init__(self, alarms):
        self.alarms = alarms
        self.label = [
            '0', '10', '20', '30', '40', '50', '60', '70', '80', '90'
        ]
        self.index = np.arange(len(self.label))

    def calculate_score_distribution(self):
        score_cnt = [0] * 10

        for alarm in self.alarms:
            score = float(alarm[4])
            if (ind := math.floor(score * 10)) == 10:
                score_cnt[9] += 1
            else:
                score_cnt[ind] += 1

        return score_cnt

    def print_score_result(self, score_cnt):
        for i in range(len(score_cnt)):
            range_str = f'{i*10}~{(i+1)*10}'
            click.echo(f'{range_str}\t', nl=False)
        click.echo()

        for score in score_cnt:
            click.echo(f'{score}\t', nl=False)
        click.echo()

    def draw_bar(self):
        score_cnt = self.calculate_score_distribution()
        self.print_score_result(score_cnt)
        plt.bar(self.index, score_cnt)

    def generate_result(self, title):
        click.echo(title)
        self.draw_bar()
        plt.title(title)
        plt.ylabel('Number of alarms')
        plt.xlabel('score')
        plt.xticks(self.index, self.label)
        plt.savefig(f'{title}_plot.png')
        plt.clf()


class TrueFalsePlotDrawer(PlotDrawer):
    def get_true_false_alarms(self):
        true_alarms = []
        false_alarms = []
        for alarm in self.alarms:
            try:
                gt = ground_truths[alarm[0]][True]
            except KeyError:
                false_alarms.append(alarm)
                continue

            src_file, src_line = alarm[2].split(':')
            sink_file, sink_line = alarm[3].split(':')

            found = False
            for t in gt:
                if t['src']['file'] == src_file and \
                   t['src']['line'] == int(src_line) and \
                   t['sink']['file'] == sink_file and \
                   t['sink']['line'] == int(sink_line):
                    found = True
                    break

            if found:
                true_alarms.append(alarm)
            else:
                false_alarms.append(alarm)

        return true_alarms, false_alarms

    def draw_bar(self):
        true_alarms, false_alarms = self.get_true_false_alarms()

        alarms = self.alarms

        self.alarms = true_alarms
        true_score_cnt = self.calculate_score_distribution()
        self.print_score_result(true_score_cnt)

        self.alarms = false_alarms
        false_score_cnt = self.calculate_score_distribution()
        self.print_score_result(false_score_cnt)

        self.alarms = alarms

        p1 = plt.bar(self.index, true_score_cnt, color='r')
        p2 = plt.bar(self.index,
                     false_score_cnt,
                     color='b',
                     bottom=true_score_cnt)
        plt.legend((p1[0], p2[0]), ('True', 'False'))


def get_elem(line, s):
    start_ind = line.find(s) + len(s) + 1
    end_ind = line.find(',', start_ind)
    return line[start_ind:end_ind]


def get_section(debian_sections, program):
    for section in debian_sections:
        if program in debian_sections[section]:
            if '/' in section:
                slash_pos = section.rfind('/')
                return section[slash_pos + 1:]
            else:
                return section[9:]


def get_ranking(popcon_ranking, program):
    for lst in popcon_ranking:
        if program in lst:
            return int(lst[0])


def generate_distribution(alarms, graph_repr):
    if graph_repr == 'default':
        drawer = PlotDrawer(alarms)
    elif graph_repr == 't/f':
        drawer = TrueFalsePlotDrawer(alarms)
    else:
        raise ArgumentError

    drawer.generate_result('HighLevel')

    bug_types = [
        '"IntOverflow."', '"FormatString."', '"BufferOverflow."',
        '"CmdInjection."', '"IntUnderflow."'
    ]
    for bug_type in bug_types:
        drawer.alarms = [alarm for alarm in alarms if alarm[1] == bug_type]
        drawer.generate_result(bug_type[1:-2])


def generate_section_statistics(section_statistics):
    selected = []
    for section, result in section_statistics.items():
        click.echo(f'Section : {section}')
        click.echo(f'NUM PACKAGES: {len(result)}')

        at_least_one = [(p, num_alarm, r) for (p, num_alarm, r) in result
                        if num_alarm > 0]
        click.echo(
            f'NUM PACKAGES WITH AT LEAST ONE ALARM : {len(at_least_one)}')

        max_true = -1
        sorted_at_least_one = sorted(at_least_one, key=lambda elem: elem[2])

        selected += sorted_at_least_one[:20]
        for i, (program, _, _) in enumerate(sorted_at_least_one):
            if program in ground_truths:
                max_true = i + 1

        click.echo(f'MAX RANK : {max_true}')

    with open(os.path.join(RESULT_DIR, 'selected-packages.txt'), 'w') as f:
        f.writelines([elem[0] + '\n' for elem in selected])


@click.command()
@click.argument('target_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--from',
              '-f',
              'from_',
              type=click.Path(exists=True, dir_okay=False))
@click.option('--graph-repr',
              type=click.Choice(['default', 't/f']),
              default='default')
def main(target_dir, from_, graph_repr):
    from_alarms = {}
    if from_:
        with open(from_, 'r') as f:
            rd = csv.reader(f)
            for line in rd:
                src = line[2]
                sink = line[3]
                from_alarms[(src, sink)] = line

    section_statistics = {}
    with open(
            os.path.join(
                RESULT_DIR,
                'debian-list-by-sections.json',
            ),
            'r',
    ) as f:
        debian_sections = json.load(f)

    with open(os.path.join(RESULT_DIR, 'popcon-install-list-clean.txt'),
              'r') as f:
        popcon_ranking = []
        for line in f.readlines():
            popcon_ranking.append([elem.strip() for elem in line.split(',')])

    num_package = 0
    num_package_with_alarm = 0
    alarms = []
    for file in os.listdir(target_dir):
        if file.endswith('.txt'):
            num_package += 1
            with open(f'{target_dir}/{file}', 'r') as f:
                program = file[:-4]
                lines = f.readlines()

                section = get_section(debian_sections, program)
                if section not in section_statistics:
                    section_statistics[section] = []
                rank = get_ranking(popcon_ranking, program)
                section_statistics[section].append((program, len(lines), rank))

                if len(lines) > 0:
                    num_package_with_alarm += 1

                for line in lines:
                    src = get_elem(line, 'src:')
                    sink = get_elem(line, 'sink:')
                    score = get_elem(line, 'score:')
                    bug_type = get_elem(line, 'bug_type:')

                    if src[0] != ':' and sink[0] != ':':
                        alarm = [program, bug_type, src, sink, score]
                        try:
                            from_alarm = from_alarms[(src, sink)]
                            alarm.append(from_alarm[5])
                            alarm.append(from_alarm[6])
                        except (KeyError, IndexError):
                            pass

                        alarms.append(alarm)

    click.echo(f'NUM PACKAGES : {num_package}')
    click.echo(
        f'NUM PACKAGES WITH AT LEAST ONE ALARM : {num_package_with_alarm}')
    click.echo(f'NUM ALARMS : {len(alarms)}')

    generate_section_statistics(section_statistics)

    with open('result.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        for alarm in alarms:
            wr.writerow(alarm)
    click.echo()

    generate_distribution(alarms, graph_repr)


if __name__ == '__main__':
    main()