#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import json
import typer
import os


def get_labels(bug_bench, program):
    split_pos = program.rfind('-')
    pname, version = program[:split_pos], program[split_pos + 1:]
    label_json_file = '{}/benchmark/{}/{}/label.json'.format(
        bug_bench, pname, version)
    labels = set()
    with open(label_json_file, 'r') as fp:
        label_json = json.load(fp)
    for label in label_json:
        labels.add((label['source']['line'], label['sink']['line']))
    return labels


def main(input_dir: Path,
         output_dir: Path,
         bug_bench: Optional[Path] = typer.Option(None)):
    os.makedirs(output_dir, exist_ok=True)
    for d in [
            name for name in os.listdir(input_dir)
            if os.path.isdir(os.path.join(input_dir, name))
    ]:
        print('Generating signatures from {}'.format(d))
        report = '{}/{}/infer-out/report.json'.format(input_dir, d)
        with open(report, 'r') as fp:
            j = json.load(fp)

        cnt = 1

        if bug_bench:
            labels = get_labels(bug_bench, d)

        for alarm in j:
            if bug_bench and (alarm['extras']['bug_src_loc']['lnum'],
                              alarm['line']) not in labels:
                continue

            if len(alarm['bug_trace']) == 0:
                continue

            os.makedirs('{}/{}'.format(output_dir, d), exist_ok=True)
            output_json = '{}/{}/{}.json'.format(output_dir, d, cnt)
            with open(output_json, 'w') as fp:
                json.dump(alarm, fp, indent=2)
            cnt += 1


if __name__ == '__main__':
    typer.run(main)
