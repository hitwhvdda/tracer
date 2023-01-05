import os
import sys

VULN_HIDX = ""
TARGET_HIDX = ""

USAGE = "python3 run-vuddy.py path_to_vuln_hidx path_to_target_hidx"


def parse_hidx(filename):
    f = open(filename, 'r')
    metadata = f.readline()
    fingerprints = []
    while True:
        fingerprint = f.readline()
        if fingerprint == '\n':
            break
        tokens = fingerprint.split()
        length = tokens[0]
        hashvals = tokens[1:]
        for hashval in hashvals:
            fingerprints.append((length, hashval))
    return fingerprints


def query(fingerprint):
    length = fingerprint[0]
    hashval = fingerprint[1]
    vuln_hidx = open(VULN_HIDX, 'r')
    while True:
        vuln_fingerprint = vuln_hidx.readline()
        if vuln_fingerprint == '\n':
            break
        vuln_tokens = vuln_fingerprint.split()
        vuln_length = vuln_tokens[0]
        vuln_hashvals = vuln_tokens[1:]
        for vuln_hashval in vuln_hashvals:
            if length == vuln_length and hashval == vuln_hashval:
                return True
    return False


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("argument error")
        print(USAGE)
    else:
        VULN_HIDX = sys.argv[1]
        TARGET_HIDX = sys.argv[2]
        fingerprints = parse_hidx(TARGET_HIDX)
        vuln_fingerprints = []
        for fingerprint in fingerprints:
            if query(fingerprint):
                vuln_fingerprints.append(fingerprint)
        print("=========================================")
        print('VULN_HIDX:', VULN_HIDX)
        print('TARGET_HIDX:', TARGET_HIDX)
        print(f'found {len(vuln_fingerprints)} vulnerabilities')
        print("result:")
        for vuln_fingerprint in vuln_fingerprints:
            print(
                f'length: {vuln_fingerprint[0]}, hash value: {vuln_fingerprint[1]}'
            )
