from paths import PROJECT_HOME, RESULT_DIR

import docker
import os
import tarfile

TMP_TAR_NAME = '/tmp/generate-size.tar'
SHELL_SC = 'generate-size.sh'

PREFIX = 'get-size'
KEYWORDS = ['ch', 'cpp', 'cc', 'vala']


def main():
    with open(os.path.join(RESULT_DIR, 'selected-packages.txt'), 'r') as f:
        packages = [line.strip() for line in f.readlines()]

    with tarfile.open(TMP_TAR_NAME, 'w') as tar:
        tar.add(os.path.join(PROJECT_HOME, 'bin', SHELL_SC), arcname=SHELL_SC)
    with open(TMP_TAR_NAME, 'rb') as f:
        tmp_tar = f.read()

    result_file = open(os.path.join(RESULT_DIR, 'selected-size.txt'), 'w')

    client = docker.from_env()

    for package in packages:
        container = client.containers.run(
            f'prosyslab/bug-bench-base',
            detach=True,
            remove=True,
            tty=True,
            stdin_open=True,
        )

        container.put_archive('/src', data=tmp_tar)

        result = container.exec_run(
            f'/src/{SHELL_SC} {package}',
            tty=True,
            privileged=True,
        )

        result = [elem.strip() for elem in result.output.split()]

        start_ind = result.index(f'{PREFIX}-start'.encode()) + 1
        cnt = 0
        for keyword in KEYWORDS:
            target_ind = result.index(f'{PREFIX}-{keyword}'.encode())
            if target_ind >= start_ind + 2:
                cnt += int(result[target_ind - 2].decode())
            start_ind = target_ind + 1

        result_file.write(f'{package} {cnt}\n')

    result_file.close()
    os.remove(TMP_TAR_NAME)


if __name__ == '__main__':
    main()