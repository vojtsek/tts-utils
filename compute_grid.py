#!/usr/bin/env python3
import os
import itertools
import sys
import subprocess
import shutil
import glob


def extract_lf0(directory):
    for fn in glob.glob(os.path.join(directory, '16k_*.wav')):
        base = '.'.join(fn.split('.')[:-1])
        if os.path.exists('{}.lf0'.format(base)):
            continue
        subprocess.call(['./extract_lf0.sh', fn, directory])


def extract_mcep(directory):
    if len(glob.glob(os.path.join(directory, '16k_*.mgc'))) > 0:
        return
    for fn in glob.glob(os.path.join(directory, '16k_*.wav')):
        base = '.'.join(fn.split('.')[:-1])
        if os.path.exists('{}.mgc'.format(base)):
            continue
        subprocess.call(['./extract_mcep.sh', fn, directory])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('working directory not provided. Exiting.')
        sys.exit(1)

    wd = sys.argv[1]
    dirs = [d for d in os.listdir(wd) if os.path.isdir(os.path.join(wd, d))]
    res_fn = 'mcd.out'
    for pair in itertools.combinations(dirs, 2):
        if not (pair[0] == "svox" or pair[1] == "svox"):
            continue
        print('Processing "{}" vs "{}"'.format(pair[0], pair[1]))
        # extract_lf0(os.path.join(wd, pair[0]))
        # extract_lf0(os.path.join(wd, pair[1]))
        extract_mcep(os.path.join(wd, pair[0]))
        extract_mcep(os.path.join(wd, pair[1]))
        if os.path.exists(res_fn):
            os.remove(res_fn)
        # cmd = ['./compute_lf0se.sh', os.path.join(wd, pair[0]), os.path.join(wd, pair[1])]
        cmd = ['./compute_mcd.sh', os.path.join(wd, pair[0]), os.path.join(wd, pair[1])]
        print(cmd)
        subprocess.call(cmd)
        # shutil.copyfile(res_fn, os.path.join(wd, '{}_vs_{}.lf0'.format(pair[0], pair[1])))
        shutil.copyfile(res_fn, os.path.join(wd, '{}_vs_{}.mgc'.format(pair[0], pair[1])))
