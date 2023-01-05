import colorama
import docker
import os
import sys
import typer

from colorama import Fore, Style

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RESULT_DIR = os.path.join(PROJECT_HOME, "result")

visited = set()


class ProcessLogger():
    def __init__(self, start, end):
        self.package_cnt = 0
        self.start = start
        self.end = end

    def add_package_cnt(self):
        self.package_cnt += 1

    def clear_previous_line(self):
        sys.stdout.write("\033[K")

    def start_analysis(self):
        print(
            Fore.GREEN + Style.BRIGHT +
            f"[+] Start analysis for {self.start+1}~{self.end} in popcon list."
        )

    def complete_analysis(self):
        self.clear_previous_line()
        print(Fore.CYAN + Style.BRIGHT + "[+] Complete analysis!")

    def log_progress(self):
        progress_num = 100 * self.package_cnt // (self.end - self.start)
        progress_str = (progress_num // 2) * '#' + (50 -
                                                    (progress_num // 2)) * '-'

        self.clear_previous_line()
        print(
            Fore.CYAN + Style.BRIGHT +
            f"[-] Progress: {progress_str} {progress_num}% {self.package_cnt}/{self.end-self.start}",
            end='\r')


def read_clean_list(lines, result):
    for line in lines:
        line = line.strip().split(',')
        key = line[1]
        if key not in result:
            result[key] = []
        for i in range(2, len(line), 2):
            package_num = int(line[i])
            package = line[i + 1]
            result[key].append((package_num, package))
            result[key].sort()
            visited.add(package_num)


def parse_source_and_version(apt_show_result):
    def parse_element(str):
        start_ind = apt_show_result.index(str) + len(str)
        end_ind = apt_show_result[start_ind:].index(b'\n') + start_ind
        return apt_show_result[start_ind:end_ind]

    if b"Source: " in apt_show_result:
        package = parse_element(b"Source: ").decode()
    else:
        package = parse_element(b"Package: ").decode()

    if b"Version: " in apt_show_result:
        version = "_" + parse_element(b"Version: ").decode()
    else:
        version = ""

    return f"{package}{version}"


def check_duplicate_sources(popcon_list, start, end, result):
    client = docker.from_env()
    base_image = "prosyslab/bug-bench-base"

    process_logger = ProcessLogger(start, end)

    process_logger.start_analysis()
    process_logger.log_progress()

    for i in range(start, end):
        if (i + 1) in visited:
            process_logger.add_package_cnt()
            process_logger.log_progress()
            continue

        line = popcon_list[i].split()
        package = line[1]
        package_num = int(line[0])

        try:
            apt_show_result = client.containers.run(base_image,
                                                    f"apt show {package}",
                                                    remove=True)

            package_src = parse_source_and_version(apt_show_result)

            if package_src not in result:
                result[package_src] = []

            result[package_src].append((package_num, package))
            result[package_src].sort()

        except docker.errors.ContainerError:
            pass
        finally:
            visited.add(i + 1)
            process_logger.add_package_cnt()

        process_logger.log_progress()

    process_logger.complete_analysis()


def generate_result(f, result_list):
    for i in range(len(result_list)):
        key = result_list[i][0]
        package_list = result_list[i][1]
        write_line = f"{i},{key}"
        for package_num, package in package_list:
            write_line = write_line + f",{package_num},{package}"
        f.write(f"{write_line}\n")


def main(start: int, end: int):
    colorama.init(autoreset=True)

    result = {}
    popcon_clean_list_path = os.path.join(RESULT_DIR,
                                          "popcon-install-list-clean.txt")
    if os.path.isfile(popcon_clean_list_path):
        with open(popcon_clean_list_path, 'r') as f:
            lines = f.readlines()
        read_clean_list(lines, result)

    popcon_list_path = os.path.join(RESULT_DIR, "popcon-install-list.txt")

    if not os.path.isfile(popcon_list_path):
        print(Fore.RED + Style.BRIGHT +
              "[!] popcon-install-list.txt does not exist in result folder.")
        sys.exit()

    with open(popcon_list_path, 'r') as f:
        popcon_list = f.readlines()

    check_duplicate_sources(popcon_list, start, end, result)

    result_list = []
    for key in result.keys():
        result_list.append([key, result[key]])

    def result_list_key(x):
        return x[1][0][0]

    result_list.sort(key=result_list_key)

    with open(popcon_clean_list_path, 'w') as f:
        generate_result(f, result_list)
        print(Fore.CYAN + Style.BRIGHT +
              "[+] popcon-install-list-clean.txt is created in result folder.")


if __name__ == "__main__":
    typer.run(main)