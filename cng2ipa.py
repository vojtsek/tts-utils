#! /usr/bin/env python3
import sys

cng2ipa = {}
with open('cng2ipa.tsv', 'r') as f:
    for line in f:
        sp = line.split('\t')
        cng2ipa[sp[0]] = sp[1]

trnfile = sys.argv[1]
content = ''
with open(trnfile, 'r') as f:
    content = f.read()
content = content.split('\n')[-1]
print(content)
