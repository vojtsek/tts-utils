#! /usr/bin/env python3
import sys

cng2ipa = {}
with open(sys.argv[2], 'r') as f:
    for line in f:
        sp = line.split('\t')
        cng2ipa[sp[0]] = sp[1].strip()

trnfile = sys.argv[1]
content = ''
with open(trnfile, 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) < 1:
            continue
        for ph in line.split():
            sys.stdout.write(cng2ipa[ph.strip('012')] + ' ')
        sys.stdout.write('\n')
