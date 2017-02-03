#! /usr/bin/env python3
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plot import SavedResults, process_data
from sklearn.linear_model import LinearRegression

def correlation(vec1, vec2, title='', x='', y=''):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    data1_mean = np.mean(vec1)
    data2_mean = np.mean(vec2)
    nom = 0
    for m1, m2 in zip(vec1, vec2):
        nom += (m1 - data1_mean) * (m2 - data2_mean)
    covariance = nom / len(vec1)
    std1 = np.std(vec1)
    std2 = np.std(vec2)
    corr = covariance / (std1*std2)
    print('Correlation: {}'.format(corr)) 
    regr = LinearRegression()
    regr.fit(vec1.reshape(vec1.shape[0], 1), vec2.reshape(vec2.shape[0], 1))
    plt.scatter(vec1, vec2, s=7)
    xx = [i/100 for i in range(35, 111)]
    yy = [regr.predict(z)[0] for z in xx]
    plt.plot(xx, yy)
    plt.xlabel(x, fontsize=18)
    plt.ylabel(y, fontsize=18)
    plt.title(title, fontsize=18)
    plt.show()

if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]

#    with open(file1, 'rb') as f:
#        data1 = pickle.load(f)

#    with open(file2, 'rb') as f:
#        data2 = pickle.load(f)
    

#    all_data1 = data1.get_data().T[:-2, :]
#    all_data2 = data2.get_data().T
    all_data1 = pd.read_csv(file1).values
    all_data2 = pd.read_csv(file2).values
    denom_mean1 = np.max(list(map(lambda x: float(x), all_data1[:,1])))
    denom_mean2 = np.max(list(map(lambda x: float(x), all_data2[:,1])))
    means1 = []
    means2 = []
    new_fn = []
    new_mean = []
    stds1 = []
    stds2 = []
    for i in range(all_data1.shape[0]):
        mean1 = float(all_data1[i,:][1])
        dd = all_data2[all_data1[i,0] == all_data2[:,0],1]
        if len(dd) == 0:
            continue
        mean2 = float(dd[0])
        nm1 = mean1 / denom_mean1
        nm2 = mean2 / denom_mean2
        means1.append(nm1)
        means2.append(nm2)
        t = 0.4
        new_fn.append(all_data1[i,:][0])
        new_mean.append(t * nm1 + (1 - t) * nm2)
    correlation(means1, means2, title='', x='MCD', y='Phnoetic distance')
