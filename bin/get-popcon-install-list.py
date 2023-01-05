import os
import requests

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RESULT_DIR = os.path.join(PROJECT_HOME, "result")


def get_popcon_list():
    url = "https://popcon.debian.org/stable/by_inst"
    response = requests.get(url)

    result_list = response.text.split('\n')

    for i in range(len(result_list)):
        if len(result_list[i]) > 0 and result_list[i][0] == '1':
            start = i
            break

    for i in range(len(result_list)):
        if "----------" in result_list[i]:
            end = i
            break

    return result_list[start:end]


if __name__ == "__main__":
    popcon_list = get_popcon_list()

    popcon_install_list_path = os.path.join(RESULT_DIR,
                                            "popcon-install-list.txt")

    with open(popcon_install_list_path, 'w') as f:
        f.write('\n'.join(popcon_list))