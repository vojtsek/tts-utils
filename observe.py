#!/usr/bin/env python3
import pandas
import sys
import os
import copy
import pickle
import numpy as np
from plot import process_data, SavedResults

def obtain_frames(dirname, fn):
    count = 0
    acc = 0
    for eng in ['cere','svox','gtts','mary']:
        ffn = os.path.join(dirname, eng,fn)
        if not os.path.exists(ffn):
            continue
        count += 1
        data = np.fromfile(ffn, dtype=np.float32).reshape((-1, 35))
        acc += len(data)
    return acc / count

if __name__ == '__main__':
    all_data = np.zeros((0, 3))
    files = sys.argv[1:]
    # assuming all files in the same directory
    dirname = os.path.dirname(files[0])
    print(dirname)
    for csvf in files:
        data = pandas.read_csv(csvf, header=None)
        fns = np.array([[csvf] for _ in range(data.shape[0])])
        data = np.concatenate((fns, data), axis=1)
        all_data = np.concatenate((all_data, data), axis=0)
        # available_counts = np.unique(data['count'].values)
    synthesizers = np.unique(all_data[:,0])
    distinct_files = np.unique(all_data[:,1])
    files = list(map(lambda x: os.path.basename(x), files))
    means = []
    stds = []
    stats_data = []
    stats_data_mean = []
    for f in distinct_files:
       f_data = all_data[all_data[:, 1] == f]
       mean = np.mean(f_data[:, 2])
       std = np.std(f_data[:, 2])
       stats_data.append([f])
       stats_data_mean.append([float(mean) / np.log(obtain_frames(dirname, f)), std])
       # means.extend([mean for _ in range(f_data.shape[0])])
       # stds.extend([std] * f_data.shape[0])
    # all_data = np.concatenate((all_data, np.array([means]).T), axis=1)
    # all_data = np.concatenate((all_data, np.array([stds]).T), axis=1)
    stats_data = np.array(stats_data)
    stats_data_mean = np.array(stats_data_mean)
    sort_perm_mean = np.argsort(stats_data_mean[:, 0], axis=0)
    sort_perm_std = np.argsort(stats_data_mean[:, 1], axis=0)
    process_data(stats_data[sort_perm_mean, 0][:-5], stats_data_mean[sort_perm_mean, 0][:-5], stats_data_mean[sort_perm_mean, 1][:-5], 'mgc-dump', files, 'results-mgc')

