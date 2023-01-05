import os
import sys
import json
import csv
import torch
from torch.utils.data import DataLoader
import numpy as np

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

dir_ = sys.argv[1]
directory = dir_
classes = []
criterion = []
trace_names = []

def parse_label(filepath):
    criterion = []
    with open(filepath,'r') as json_file:
        json_data = json.load(json_file)
        t = json_data['trace']
        for i in t:
            if str(type(i[0][-1])) == "<class 'bool'>":
                if i[0][-1]:
                    i[0][-1] = "1"
                else:
                    i[0][-1] = "0"
                ans = "_".join(i[0])
            else:
                ans = "_".join(i[0])
            if ans[-1] == '\n':
                ans = ans[:-1]
            criterion.append(ans)
    criterion = list(set(criterion))
    name = json_data['id']
    if name[-1] == '\n':
        name = name[:-1]
    return criterion, name

def record_init():
    labels = []
    criterion = []
    trace_names = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        labels.append(filename.split('-')[0])
        c, n = parse_label(filepath)
        criterion.extend(c)
        trace_names.append(n)
    classes = list(set(labels))
    criterion = list(set(criterion))
    return classes, criterion, trace_names

def make_x():
    classes, criterion, trace_names = record_init()
    labels = []
    x_base = [[-1 for _ in range(len(criterion))] for _i in range(len(trace_names))]
    for filename in trace_names:
        if filename[-1] == '\n':
            filepath = directory + "/" + filename[:-1] + ".json"
        else:
            filepath = directory + "/" + filename + ".json"
        labels.append(classes.index(filename.split('-')[0]))
        with open(filepath,'r') as json_file:
            json_data = json.load(json_file)
            t = json_data['trace']
            for i in t:
                if str(type(i[0][-1])) == "<class 'bool'>":
                    if i[0][-1]:
                        i[0][-1] = "1"
                    else:
                        i[0][-1] = "0"
                    cr = "_".join(i[0])
                else:
                    cr = "_".join(i[0])
                x_base[trace_names.index(filename)][criterion.index(cr)] = i[1]
        for j in range(len(x_base[0])):
            if  x_base[trace_names.index(filename)][j] < 0:
                x_base[trace_names.index(filename)][j] = 0
    return x_base, labels


x_, y_ = make_x()
clf = DecisionTreeClassifier()
scores = cross_val_score(estimator=clf, X=x_, y=y_, cv=7, n_jobs=4)
print(np.mean(np.array(scores)))