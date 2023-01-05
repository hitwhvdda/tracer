from paths import RESULT_DIR

import click
import matplotlib.pyplot as plt
import os


class InvalidAnalysisError(Exception):
    pass


def get_selected_size():
    with open(os.path.join(RESULT_DIR, 'selected-size.txt'), 'r') as f:
        selected_size = []
        for line in f.readlines():
            package, size = line.split()
            size = int(size)

            selected_size.append((package, size))

    return dict(selected_size)


def get_tracer_time(tracer_result):
    result = {}
    with open(tracer_result, 'r') as f:
        for line in f.readlines():
            package, _, time = line.split()
            time = float(time)
            result[package] = time
    return result


def convert_time(time):
    result = 0

    base_index = 0
    while base_index < len(time):
        num_index = base_index
        while time[num_index].isdigit() or time[num_index] == '.':
            num_index += 1
        digit = float(time[base_index:num_index])

        word_index = num_index
        while word_index < len(time) and time[word_index].isalpha():
            word_index += 1
        unit = time[num_index:word_index]

        if unit == 'min':
            c = 60
        elif unit == 's':
            c = 1
        elif unit == 'ms':
            c = 0.001

        result += digit * c

        base_index = word_index

    return result


def get_infer_analysis_time(infer_log):
    with open(infer_log, 'r') as f:
        found = False
        for line in f.readlines():
            if 'Analysis phase finished in' in line:
                found = True
                time = line.split()[-1]
                break

        if not found:
            raise InvalidAnalysisError()

    return convert_time(time)


def generate_plot(result, extension):
    sizes = []
    times = []

    for (size, time) in result.values():
        sizes.append(size / 1000000)
        times.append(time)

    plt.xlabel('Size of program (MLOC)', fontsize=16)
    plt.ylabel('Time(s)', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.scatter(sizes, times, s=100, marker='+', color='b')
    plt.savefig(f'scalability.{extension}', bbox_inches='tight', pad_inches=0)


@click.command()
@click.argument('infer-result', type=click.Path(exists=True, file_okay=False))
@click.option('--tracer-result', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '--result-extension',
    type=click.Choice(['png', 'pdf']),
    default='png',
)
def main(infer_result, tracer_result, result_extension):
    selected_size = get_selected_size()
    if tracer_result:
        tracer_time = get_tracer_time(tracer_result)

    result = {}

    for package in os.listdir(infer_result):
        infer_log = os.path.join(infer_result, package, 'infer-out', 'logs')
        if os.path.exists(infer_log):

            try:
                time = get_infer_analysis_time(infer_log)
                if tracer_result:
                    time += tracer_time[package]
                size = selected_size[package]
                result[package] = (size, time)
            except InvalidAnalysisError:
                click.secho(
                    f'[!] Analysis for {package} is incomplete!',
                    fg='red',
                )
                continue

    generate_plot(result, result_extension)


if __name__ == '__main__':
    main()