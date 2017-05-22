import pandas
import sys
import matplotlib.pyplot as plt
import numpy as np


def sort_data_by_column(data, col):
    sortperm = np.argsort(data[:,col])
    return data[sortperm]

def split_data_into_bins(d1, d2):
    bins = np.unique(d1)
    data = []
    for b in bins:
        data.append(list(d2[d1 == b]))
    return data, bins

def boxplot(binned_data):
    bx = plt.boxplot(binned_data, notch=False, vert=True, patch_artist=True, sym='x', whis=.5)
    plt.setp(bx['boxes'], color='black')
    plt.setp(bx['whiskers'], color='black')
    plt.setp(bx['fliers'], color='black')
    plt.setp(bx['caps'], color='black')
    plt.setp(bx['medians'], color='orange', linewidth=2)
    for patch in bx['boxes']:
        patch.set_facecolor('lightblue')

data = pandas.read_csv(sys.argv[1])

gold_data = data[data['type'] != 'gold']
gold_data_by_data_size = sort_data_by_column(gold_data.values, 3)
gold_data_by_layer_size = sort_data_by_column(gold_data.values, 2)
gold_data_by_epochs = sort_data_by_column(gold_data.values, 1)
#binned_data, bins = split_data_into_bins(gold_data_by_epochs[:,1], gold_data_by_epochs[:,4])
#binned_data, bins = split_data_into_bins(gold_data_by_layer_size[:,2], gold_data_by_layer_size[:,4])
binned_data, bins = split_data_into_bins(gold_data_by_data_size[:,3], gold_data_by_data_size[:,4])
boxplot(binned_data)

name = 'Neural network, gold not included\n Data Size vs Accuracy'
plt.xlabel('Data Size')
plt.ylabel('Accuracy')
plt.xticks([1 + x for x in range(len(bins))], bins)
plt.title(name)
#plt.show()
plt.savefig(name.replace(' ', '_') + '.jpg')
