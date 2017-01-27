#!/usr/bin/env python3
import sys
import os
import pickle
import numpy as np
import glob
import matplotlib.pyplot as plt

split1 = 13
split2 = 18
split3 = 25
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
        print(self.name)
        return self.name

    def get_by_fn(self, fn):
        return self.data[self.data[:,0] == fn][0]

def get_color(mean, std):
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
    page += '[{}] <a style="color:{};" href={}/{}.wav>{}</a>&nbsp;'.format(mean, color, engine, fn, engine)
    return page

def plot_one_recording(fn, dumpdir):
    means = []
    fns = []
    stds = []
    b_width = 0.3
    for dump in glob.glob('{}/*'.format(dumpdir)):
        fns.append(dump.lstrip('dump/'))
        with open(dump, 'rb') as f:
            data = pickle.load(f)
            dfn = data.get_by_fn(fn)
            means.append(float(dfn[1]))
            stds.append(float(dfn[2]))
    index = np.arange(len(fns))
    plt.bar(index, means, b_width, color='blue', alpha=0.5, align='center', yerr=stds, label='MCD')
    plt.xlabel('Engines used')
    plt.ylabel('MCD')
    plt.title('MCD value of \'{}\' for particular settings'.format(fn))
    plt.xticks(index, fns)
    plt.legend()

    plt.tight_layout()
    plt.show()

def process_data(name_data, mean_data, std_data, dirname, files, outname):
    saved_data = SavedResults(name_data, mean_data, std_data, '_'.join(files))
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    with open('{}/{}'.format(dirname, saved_data.get_name()), 'wb') as f:
        pickle.dump(saved_data, f)

    page = '<html><body>'
    for fn, mean, std in zip(name_data, mean_data, std_data):
    #    print(fn[0], end=' ')
    #    print(val)
        page += fn + '&nbsp;'
        for eng in ['cere', 'flite', 'svox', 'mary', 'gtts']:
            page = create_link(eng, fn, page, mean, std)
        page += '<br />'
    page += '</body></html>'
    with open('{}.html'.format(outname), 'w') as f:
        f.write(page)
    plt.hist(mean_data, bins=70, range=(10,40), alpha=.3, color='gray')
    plt.axvline(x=split1, ymin=0, ymax=500, linewidth=3, color='green')
    plt.axvline(x=split2, ymin=0, ymax=500, linewidth=3, color='pink')
    plt.axvline(x=split3, ymin=0, ymax=500, linewidth=3, color='red')
    #plt.show()
    print(fn)
    plt.close()

if __name__ == '__main__':
    fn = sys.argv[1]
