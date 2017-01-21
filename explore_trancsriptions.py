#! /usr/bin/env python3
import json
import os
import sys
import glob
import numpy as np
import editdistance as ed
import itertools as itt

from plot import process_data

def get_file_name(path):
    return '_'.join('.'.join(os.path.basename(path).split('.')[:-1]).split('_')[1:])

def get_transcriptions_for_recording(fn, data, label):
    with open(fn, 'r') as f:
        content = f.read()
        file_name = get_file_name(fn)
        data.append([label, file_name, content])

def get_data_for_filename(fn, data):
    return data[data[:, 1] == fn]

def unzip(seq, idx):
    return np.array(list(map(lambda x: x[idx], seq)))

def process_file(fn, data):
    all_trns = []
    for record in get_data_for_filename(fn, data):
        trns = list(map(lambda x: x['transcription'], json.loads(record[2])))
        all_trns.extend(trns)

    combs = []
    denom = np.log(len(fn)) + 1
    for comb in itt.combinations(all_trns, 2):
        combs.append(ed.eval(*comb) / denom)
    
    mean = sum(combs) / len(combs)
    std_sum = 0
    for comb in combs:
        std_sum += np.power(comb - mean, 2)
    return mean, np.sqrt(std_sum / len(combs))

def process_all(all_files, data):
    res = []
    for fn in all_files:
        res.append((fn, *process_file(fn, data)))
    return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Directory with hypothesis not provided.')
        sys.exit(1)
    dirname = os.path.abspath(sys.argv[1])
    dirs = list(filter(lambda x: os.path.isdir(os.path.join(dirname, x)), os.listdir(dirname)))
    data = []
    all_files = set()
    for directory in dirs:
        print('Processing {}'.format(directory))
        for fn in glob.glob(os.path.join(dirname, directory, '*.json')):
            all_files.add(get_file_name(fn))
            get_transcriptions_for_recording(fn, data, directory)

    data = np.array(data)
    res = sorted(process_all(all_files, data), key=lambda x: x[1])
    process_data(unzip(res, 0), unzip(res, 1), unzip(res, 2), 'trn-dump', dirs, 'results-trns')

