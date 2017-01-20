#! /usr/bin/env python3
import json
import os
import sys
import glob
import numpy as np
import editdistance as ed
import itertools as itt

def get_file_name(path):
    return '_'.join('.'.join(os.path.basename(path).split('.')[:-1]).split('_')[1:])

def get_transcriptions_for_recording(fn, data, label):
    with open(fn, 'r') as f:
        content = f.read()
        file_name = get_file_name(fn)
        data.append([label, file_name, content])

def get_data_for_filename(fn, data):
    return data[data[:, 1] == fn]

def process_file(fn, data):
    all_trns = []
    for record in get_data_for_filename(fn, data):
        trns = list(map(lambda x: x['transcription'], json.loads(record[2])))
        all_trns.extend(trns)

    ed_sum = 0
    for comb in itt.combinations(all_trns, 2):
        ed_sum += ed.eval(*comb)
    return ed_sum / (np.log(len(fn)) + 1)

def process_all(all_files, data):
    res = []
    for fn in all_files:
        res.append((fn, process_file(fn, data)))
    return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Directory with hypothesis not provided.')
        sys.exit(1)
    dirname = sys.argv[1]
    dirs = filter(lambda x: os.path.isdir(x), os.listdir(dirname))
    data = []
    all_files = set()
    for directory in dirs:
        print('Processing {}'.format(directory))
        for fn in glob.glob(os.path.join(directory, '*.json')):
            all_files.add(get_file_name(fn))
            get_transcriptions_for_recording(fn, data, directory)

    data = np.array(data)
    res = sorted(process_all(all_files, data), key=lambda x: x[1])
    print(res)

