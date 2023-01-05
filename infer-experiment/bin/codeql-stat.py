import os
import csv
from ground_truths import ground_truths
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='generate codeql statistics')

parser.add_argument('--in_dir', type=str, 
                    help='an input folder for codeql statistics', default="../codeql/codeql-home/result")

parser.add_argument('--out_dir', type=str, 
                    help='an output folder for codeql statistics', default="../codeql/result")

parser.add_argument('--packages', type=str, 
                    help='an output folder for codeql statistics', default="../result/selected-packages.txt")

args = parser.parse_args()

directory=args.in_dir
result_dir=args.out_dir
packages = args.packages
codeql_total=args.out_dir + "/codeql-total.csv"
codeql_truth=args.out_dir + "/codeql-truth.csv"
codeql_false=args.out_dir + "/codeql-false.csv"
selected_list=[]
package_list=[]
final=[]
for i in ground_truths:
    selected_list.append(i)

f = open(packages, 'r')
while True:
    line = f.readline()
    if not line: break
    package_list.append(line.strip())
f.close()

def count_total(truth_list):
    total_cnt=0
    codeql = open(codeql_total, 'w', newline='')
    wr = csv.writer(codeql)
    codeql_f = open(codeql_false, 'w', newline='')
    wr2 = csv.writer(codeql_f)
    for bench in os.listdir(directory):
        if bench not in package_list:
            continue
        benchdir = os.path.join(directory, bench)
        for filename in os.listdir(benchdir):
            filepath=os.path.join(benchdir, filename)
            with open(filepath, 'r') as csvfile:
                datareader=csv.reader(csvfile)
                for row in datareader:
                    if (row[2] == "error"):
                        total_cnt += 1
                        wr.writerow([bench, (filename.split('-')[-1]).split('.')[0], row])
                        if row not in truth_list:
                            wr2.writerow([bench, (filename.split('-')[-1]).split('.')[0], row])
    print(total_cnt)
    codeql.close()
    codeql_f.close()

def count_truth():
    total_truth=0
    truth_list = []
    f_t = open(codeql_truth, 'w', newline='')
    wr = csv.writer(f_t)
    for bench in os.listdir(directory):
        if bench not in selected_list:
            continue
        gt_lst=[]
        for i in ground_truths[bench][True]:
            gt_lst.append((i['sink']['file'], int(i['sink']['line'])))
        benchdir = os.path.join(directory, bench)
        for filename in os.listdir(benchdir):
            filepath=os.path.join(benchdir, filename)
            with open(filepath, 'r') as csvfile:
                datareader=csv.reader(csvfile)
                for row in datareader:
                    if (row[2] == "error"):
                        src = row[4][1:]
                        line = int(row[5])
                        if (src, line) in gt_lst:
                            total_truth+=1
                            wr.writerow([bench, (filename.split('-')[-1]).split('.')[0], row])
                            truth_list.append(row)
    print(total_truth)
    f_t.close()
    return truth_list

if __name__ == "__main__":
    truth_list = count_truth()
    count_total(truth_list)