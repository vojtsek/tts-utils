#! /usr/bin/env python3
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plot import SavedResults, process_data
from correlation import correlation

if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    labels = sys.argv[3]

    with open(file1, 'rb') as f:
        data1 = pickle.load(f)

    with open(file2, 'rb') as f:
        data2 = pickle.load(f)
    
    labels = pd.read_csv(labels, sep=',', header=None)
    all_data1 = data1.get_data().T[:-2, :]
    all_data2 = data2.get_data().T
    denom_mean1 = np.max(list(map(lambda x: float(x), all_data1[:,1])))
    denom_mean2 = np.max(list(map(lambda x: float(x), all_data2[:,1])))
    means1 = []
    means2 = []
    new_fn = []
    new_std = []
    new_mean = []
    stds1 = []
    stds2 = []
    colors = []
    judges = []
    for i in range(all_data1.shape[0]):
        name = all_data1[i,0][:-4]
        mean1 = float(all_data1[i,:][1])
        mean2 = float(data2.get_by_fn(all_data1[i,:][0], True)[1])
        labeled = name in labels.values[:,0]
        if labeled:
            lv = labels.values
            l = [int(i) for i in list(lv[lv[:,0]==name][0])[1:]]
            mm = np.mean(l)
            nm1 = mean1
            nm2 = mean2
            lvl = 1
            if mm < 1.75:
                if lvl < 2:
                    judges.append(mm)
                    colors.append('g')
                    means1.append(nm1)
                    means2.append(nm2)
            elif mm < 2.5:
                if lvl < 3:
                    judges.append(mm)
                    colors.append('b')
                    means1.append(nm1)
                    means2.append(nm2)
            else:
                judges.append(mm)
                colors.append('r')
                means1.append(nm1)
                means2.append(nm2)
            t = 0.4
            new_fn.append(all_data1[i,:][0])
            new_mean.append(t * nm1 + (1 - t) * nm2)
            new_std.append(all_data1[i,:][2])
    argperm = np.argsort(new_mean)
    new_fn = np.array(new_fn)[argperm]
    new_mean = np.array(new_mean)[argperm]
    new_std = np.array(new_std)[argperm]
    judges = np.array(judges) - min(judges)
    judges = judges / max(judges)
    means1 = np.array(means1) - min(means1)
    means1 = np.array(means1) / max(means1)
    means2 = np.array(means2) / max(means2)
    correlation(judges, means1, title="", x="labeling", y="MCD", color=colors)
    # process_data(all_data2[:,0], all_data2[:, 1], all_data2[:,2], '/tmp/dump', ['ss','dd'], '/tmp/results')
    # process_data(new_fn, new_mean, new_std, 'combined-dump', ['cere','svox', 'gtts'], 'results-combined')
        
