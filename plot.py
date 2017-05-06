#!/usr/bin/env python3
import sys
import os
import pickle
import numpy as np
import glob
import matplotlib.pyplot as plt

split1 = 0.2
split2 = 0.3
split3 = 0.45
class SavedResults:

    def __init__(self, data, mean_data, std_data, name):
        data = np.array([data])
        mean_data = np.array([mean_data])
        std_data = np.array([std_data])
        self.data = np.concatenate((data, mean_data, std_data), axis=0)
        name_set = set([n.rstrip('.mgc') for n in name.split('_') if n not in ('vs', 'clean', 'flag')])
        self.name = '_'.join(list(name_set))

    def get_data(self):
        return self.data

    def get_name(self):
        return self.name

    def get_by_fn(self, fn, transposed=False):
        fn = fn.split('.')
        if len(fn) > 1:
            fn = fn[:-1]
        fn = '.'.join(fn).lstrip()
        if fn.startswith('16k_'):
            fn = fn[4:]
        if transposed:
            data = self.data.T
        else:
            data = self.data
        for i in range(data.shape[0]):
            if fn in data[i,:][0]:
                return data[i, :]
        return None

def get_color(mean, std):
    mean = float(mean)
    if (mean < split1):
        return "green"
    elif (mean < split2):
        return "lime"
    elif (mean < split3):
        return "pink"
    else:
        return "red"


def create_link(engine, fn, page, mean, std):
    color = get_color(mean, std)
    fn = fn.split('.')
    if len(fn) > 1:
        fn = fn[:-1]
    fn = '.'.join(fn)
    page += '<a style="color:{};" href=backers/{}/{}.wav>{}</a>&nbsp;'.format(color, engine, fn, engine)
    return page

def get_MCD_for_name_for_synth(fn, dumpdir):
    pairs = []
    all_synth = None
    for dump in glob.glob('{}/*'.format(dumpdir)):
        with open(dump, 'rb') as f:
            sp = [fn.strip('./') for fn in dump.split('_')]
            l = len(sp)
            if l == 3:
                continue
            data = pickle.load(f)
            dfn = data.get_by_fn(fn)
            mean = float(dfn[1])
            std = float(dfn[2])
            if l == 2:
                pairs.append((sp, mean))
            if l == 4:
                all_synth = mean
    for eng in ['mary','svox','gtts','cere']:
        s = sum([p[1] for p in pairs if eng not in p[0]]) / (len(pairs) - 3)
        print('Without {}: {}'.format(eng, s))
    print(sum([p[1] for p in pairs]) / len(pairs), all_synth)

def plot_two_recordings(fn1, fn2, dumpdir):
    means1 = []
    fns = []
    stds1 = []
    means2 = []
    stds2 = []
    b_width = 0.3
    for dump in glob.glob('{}/*'.format(dumpdir)):
        fns.append(dump[2:])
        with open(dump, 'rb') as f:
            data = pickle.load(f)
            dfn1 = data.get_by_fn(fn1)
            dfn2 = data.get_by_fn(fn2)
            means1.append(float(dfn1[1]))
            stds1.append(float(dfn1[2]))
            means2.append(float(dfn2[1]))
            stds2.append(float(dfn2[2]))
    tr_fns = list(map(lambda x: len(x.split('_')), fns))
    sortperm = np.argsort(tr_fns)
    fns = list(map(lambda x: x.replace('_','\n'), fns))
    fns = np.array(fns)[sortperm]
    means1 = np.array(means1)[sortperm]
    means2 = np.array(means2)[sortperm]
    stds1 = np.array(stds1)[sortperm]
    stds2 = np.array(stds2)[sortperm]
    index = np.arange(len(fns))
    plt.bar(index, means1, b_width, color='blue', alpha=0.5, align='center', yerr=stds1, label=fn1)
    plt.bar(index + b_width, means2, b_width, color='red', alpha=0.5, align='center', yerr=stds2, label=fn2)
    plt.xlabel('Engines used')
    plt.ylabel('M1')
    plt.title('M1 values of \'{}\' and \'{}\' for combinations of engines'.format(fn1, fn2))
    plt.xticks(index, fns, fontsize=18)
    plt.legend(fontsize=18)

    plt.tight_layout()
    plt.show()

def get_split(d, p):
    d = sorted(d)
    idx = int(len(d) * p)
    return d[idx]

def process_data(name_data, mean_data, std_data, dirname, files, outname, plot=True):
    saved_data = SavedResults(name_data, mean_data, std_data, '_'.join(files))
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    with open('{}/{}'.format(dirname, saved_data.get_name()), 'wb') as f:
        pickle.dump(saved_data, f)

    split1 = get_split(mean_data, 0.05)
    split2 = get_split(mean_data, 0.5)
    split3 = get_split(mean_data, 0.95)
    page = '<html><body>'
    for fn, mean, std in zip(name_data, mean_data, std_data):
        page += '{} [{}]&nbsp;'.format(fn, mean)
        for eng in ['cere', 'flite', 'svox', 'mary', 'gtts']:
            page = create_link(eng, fn, page, mean, std)
        page += '<br />'
    page += '</body></html>'
    with open('{}.html'.format(outname), 'w') as f:
        f.write(page)
    if plot:
        plt.hist(mean_data, bins=70,  alpha=.3, color='gray')
        plt.axvline(x=split1, ymin=0, ymax=500, linewidth=3, color='green')
        plt.axvline(x=split2, ymin=0, ymax=500, linewidth=3, color='pink')
        plt.axvline(x=split3, ymin=0, ymax=500, linewidth=3, color='red')
        plt.show()
        plt.close()

        plt.plot(np.arange(len(mean_data)), mean_data)
        plt.show()

def get_idx_of(n, data):
    return np.where(n == data)[0]

def plot_data(fn1, fn2):
    with open(fn1, 'rb') as f:
        data1 = pickle.load(f).get_data().T
        #length1 = int(data1.shape[0] / 3)
        #fn1 = data1[0:length1]
        #mean1 = data1[length1:2*length1]
        fn1 = data1[:,0]
        mean1 = np.array(data1[:,1], dtype='float32')
    sort_perm = []
    with open(fn2, 'rb') as f:
        data2 = pickle.load(f).get_data().T
        #length2 = int(data2.shape[0] / 3)
        #tmp_fn2 = data2[0:length2]
        #tmp_mean2 = data2[length2:2*length2]
        fn2 = np.array(['16k_' + fn + '.mgc' for fn in data2[:,0]])
        mean2 = np.array(data2[:,1], dtype='float32')
    all_fn = list(set(fn1).intersection(set(fn2)))
    f1 = []
    m1 = []
    f2 = []
    m2 = []
    for i in range(len(all_fn)):
        f1.append(all_fn[i])
        f2.append(all_fn[i])
        idx = get_idx_of(all_fn[i], fn1)
        idx2 = get_idx_of(all_fn[i], fn2)
        m1.append(mean1[idx][0])
        m2.append(mean2[idx2][0])
        sort_perm.append(idx)
    mean1 = np.array(m1, dtype='float32').T
    mean2 = np.array(m2, dtype='float32').T
    mean1 = mean1 / max(mean1)
    mean2 = mean2 / max(mean2)
    fn1 = np.array(f1[:-5])
    perm1 = np.argsort(mean1)
    perm2 = np.argsort(mean2)
    mean1 = mean1[perm1]
    mean1 = mean1[:-5]
    fn2 = np.array(f2[:-5])
    mean2 = mean2[perm1]
    mean2 = mean2[:-5]
    print(len(mean1), len(mean2))
    plt.plot([i for i in range(0, mean1.shape[0], 4)], [sum(mean2[i:i+4])/4 for i in range(0, mean1.shape[0], 4)], linewidth=.2)
    plt.plot(np.arange(mean1.shape[0]), mean1, linewidth=3)
    plt.show()

if __name__ == '__main__':
    fn1 = sys.argv[1]
    fn2 = sys.argv[2]
    dumpdir = sys.argv[3]
    # plot_data(fn1, fn2)
    get_MCD_for_name_for_synth(fn1, dumpdir)
    plot_two_recordings(fn1, fn2, dumpdir)
