from pathlib import Path
import json
import os
import typer


def log_fail_case(ind, num_trace):
    typer.secho(f"{ind} : {num_trace}", fg=typer.colors.BRIGHT_YELLOW)


def main(target_dir: Path = typer.Argument(
    ...,
    exists=True,
    dir_okay=True,
    readable=True,
)):
    typer.secho(
        f"[+] Start scanning {target_dir}...",
        fg=typer.colors.BRIGHT_GREEN,
    )

    zero_trace = 0
    one_trace = 0
    more_trace = 0
    for dir in os.listdir(target_dir):
        report_json = os.path.join(target_dir, dir, 'infer-out', 'report.json')
        if os.path.isfile(report_json):
            typer.secho(f"[-] Scanning {dir}...",
                        fg=typer.colors.BRIGHT_YELLOW)
            with open(report_json, 'r') as f:
                report = json.load(f)

                for i, alarm in enumerate(report):
                    num_trace = len(alarm['bug_trace'])
                    if num_trace == 0:
                        zero_trace += 1
                        log_fail_case(i, num_trace)
                    elif num_trace == 1:
                        one_trace += 1
                    else:
                        more_trace += 1
                        log_fail_case(i, num_trace)

    typer.secho(
        f"[+] Result : zero trace = {zero_trace}, one trace = {one_trace},"
        f" more than one trace = {more_trace}",
        fg=typer.colors.BRIGHT_BLUE,
    )
    if zero_trace == 0 and more_trace == 0:
        typer.secho(f"[+] Test passed!", fg=typer.colors.BRIGHT_GREEN)
    else:
        typer.secho(f"[+] Test failed...", fg=typer.colors.BRIGHT_RED)


if __name__ == "__main__":
    typer.run(main)