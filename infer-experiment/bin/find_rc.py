import ground_truths as gt

import json

with open('result/selected-packages.txt', 'r') as f:
    packages = [p.strip() for p in f.readlines()]
    packages.sort()

bug_types = [
    '"BufferOverflow."', '"CmdInjection."', '"DoubleFree."', '"FormatString."',
    '"IntOverflow."', '"IntUnderflow."', '"UseAfterFree."'
]


def get_rc(package, bug_type):
    alarms = {}
    with open(f'../tracer/tracer-pulse/{package}.txt') as f:
        j = open(f'../tracer/tracer-pulse/{package}.json')
        json_data = json.load(j)

        lines = f.readlines()
        for line in lines:
            data = line.split()
            src = data[2][:-1]
            sink = data[4][:-1]

            score = float(data[6][:-1])
            bt = data[8]
            if bt != bug_type:
                continue

            true_alarms = []
            if package in gt.ground_truths and True in gt.ground_truths[
                    package]:
                true_alarms = gt.ground_truths[package][True]
            is_true = False
            for true_alarm in true_alarms:
                if src == f'{true_alarm["src"]["file"]}:{true_alarm["src"]["line"]}' and sink == f'{true_alarm["sink"]["file"]}:{true_alarm["sink"]["line"]}':
                    is_true = True
                    break
            if not is_true:
                continue

            found = False
            for d in json_data:
                if not d['weighted_traces']:
                    continue
                build_src = f"{d['weighted_traces'][0]['trace'][0]['file']}:{d['src']}"
                build_sink = f"{d['weighted_traces'][0]['trace'][-1]['file']}:{d['weighted_traces'][0]['trace'][-1]['line']}"
                if build_src == src and build_sink == sink:
                    sig = d['weighted_traces'][0]['signature']
                    found = True
                    break
            if not found:
                print(package, src, sink)

            if sink not in alarms:
                alarms[sink] = (set([src]), score, score, sig)
            else:
                new_src = alarms[sink][0] | set([src])
                if alarms[sink][1] > score:
                    new_sig = alarms[sink][3]
                else:
                    new_sig = sig
                new_max_score = max(alarms[sink][1], score)
                new_min_score = min(alarms[sink][2], score)
                alarms[sink] = (new_src, new_max_score, new_min_score, new_sig)

    result = []
    for p in alarms:
        found = False
        for rc in result:
            if rc[0] & alarms[p][0]:
                result.remove(rc)
                result.append(
                    (rc[0] | alarms[p][0], max(rc[1], alarms[p][1]),
                     min(rc[2], alarms[p][2]),
                     rc[3] if rc[1] > alarms[p][1] else alarms[p][3]))
                found = True
                break
        if not found:
            result.append(alarms[p])

    max_score = 0
    min_score = 1
    signature = None
    if result:
        for _, mxs, mns, sg in result:
            signature = sg if mxs > max_score else signature
            max_score = max(max_score, mxs)
            min_score = min(min_score, mns)

        print(
            f'{package} {len(result)} {bug_type} {min_score}-{max_score} {signature}'
        )
    return len(result)


if __name__ == '__main__':
    cnt = 0
    for package in packages:
        for bug_type in bug_types:
            cnt += get_rc(package, bug_type)
    print(cnt)