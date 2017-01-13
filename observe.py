#!/usr/bin/env python3
import pandas
import sys
import os
import copy
import pickle
import numpy as np
import matplotlib.pyplot as plt


class SavedResults:

    def __init__(self, data, mean_data, perm, name):
        self.data = np.concatenate((data[perm], mean_data[perm]), axis=1)
        name_set = set([n.rstrip('.mgc') for n in name.split('_') if n not in ('vs', 'clean', 'flag')])
        self.name = '_'.join(list(name_set))

    def get_data(self):
        return self.data

    def get_name(self):
        return self.name

    def get_by_fn(self, fn):
        return self.data[self.data[:,0] == fn][0]

split1 = 13
split2 = 18
split3 = 25
def get_color(val):
    if (val[0] < split1):
        return "green"
    elif (val[0] < split2):
        return "lime"
    elif (val[0] < split3):
        return "pink"
    else:
        return "red"


def create_link(engine, fn, page, value):
    color = get_color(value)
    fn = '.'.join(fn.split('.')[:-1])
    page += '<a style="color:{};" href={}/{}.wav>{}</a>&nbsp;'.format(color, engine, fn, engine)
    return page

def obtain_frames(fn):
    count = 0
    acc = 0
    for eng in ['cere','svox','gtts','mary']:
        ffn = os.path.join(eng,fn)
        if not os.path.exists(ffn):
            continue
        count += 1
        data = np.fromfile(ffn, dtype=np.float32).reshape((-1, 35))
        acc += len(data)
    return np.exp(1)
    return acc / count

if __name__ == '__main__':
    all_data = np.zeros((0, 3))
    files = sys.argv[1:]
    for csvf in files:
        data = pandas.read_csv(csvf, header=None)
        fns = np.array([[csvf] for _ in range(data.shape[0])])
        data = np.concatenate((fns, data), axis=1)
        all_data = np.concatenate((all_data, data), axis=0)
        # available_counts = np.unique(data['count'].values)
    synthesizers = np.unique(all_data[:,0])
    distinct_files = np.unique(all_data[:,1])
    means = []
    stds = []
    stats_data = []
    stats_data_mean = []
    for f in distinct_files:
       f_data = all_data[all_data[:, 1] == f]
       mean = np.mean(f_data[:, 2])
       std = np.std(f_data[:, 2])
       stats_data.append([f])
       stats_data_mean.append([float(mean) / np.log(obtain_frames(f)), std])
       # means.extend([mean for _ in range(f_data.shape[0])])
       # stds.extend([std] * f_data.shape[0])
    # all_data = np.concatenate((all_data, np.array([means]).T), axis=1)
    # all_data = np.concatenate((all_data, np.array([stds]).T), axis=1)
    stats_data = np.array(stats_data)
    stats_data_mean = np.array(stats_data_mean)
    sort_perm_mean = np.argsort(stats_data_mean[:, 0], axis=0)
    sort_perm_std = np.argsort(stats_data_mean[:, 1], axis=0)
    saved_data = SavedResults(stats_data, stats_data_mean, sort_perm_mean, '_'.join(files))
    with open('dump/{}'.format(saved_data.get_name()), 'wb') as f:
        pickle.dump(saved_data, f)

    page = '<html><body>'
    for fn, val in zip(stats_data[sort_perm_mean], stats_data_mean[sort_perm_mean]):
    #    print(fn[0], end=' ')
    #    print(val)
        page += fn[0] + '&nbsp;'
        page = create_link('cere', fn[0], page, val)
        page = create_link('flite', fn[0], page, val)
        page = create_link('svox', fn[0], page, val)
        page = create_link('mary', fn[0], page, val)
        page = create_link('gtts', fn[0], page, val)
        page += '<br />'
    page += '</body></html>'
    with open('result.html', 'w') as f:
        f.write(page)
    plt.hist(stats_data_mean[:,0], bins=70, range=(10,40), alpha=.3, color='gray')
    plt.axvline(x=split1, ymin=0, ymax=500, linewidth=3, color='green')
    plt.axvline(x=split2, ymin=0, ymax=500, linewidth=3, color='pink')
    plt.axvline(x=split3, ymin=0, ymax=500, linewidth=3, color='red')
    #plt.show()
    plt.close()
