#! /usr/bin/env python3
import sys

def create_ssml(phonemes, fd):
    fd.write('<s>\n')
    for ph in phonemes.split():
        if 'SIL' in ph:
            fd.write('<break></break>')
        elif ph != ' ':
            fd.write('<phoneme alphabet="ipa" ph="{}">{}</phoneme>'.format(ph, ph))
    fd.write('</s>\n')


def ignore(char):
    return char in ['\'', '-']


cng2ipa = {}
mapfile = 'cng2ipa.tsv'
if len(sys.argv) > 2:
    mapfile = sys.argv[2]
with open(mapfile, 'r') as f:
    for line in f:
        sp = line.strip().split('\t')
        cng2ipa[sp[0]] = sp[1]

trnfile = sys.argv[1]
content = ''
with open(trnfile, 'r') as f:
    content = f.read()
trn = content.split('\n')[0]
pos = 0
ipatrn = ''
while pos < len(trn):
    char = trn[pos:pos+2]
    if char in cng2ipa:
        ipatrn += cng2ipa[char] + ' '
        pos += 2
    else:
        char = trn[pos]
        pos += 1
        if ignore(char):
            continue
        elif char == ' ':
            #ipatrn += ' SIL '
            pass
        else:
            ipatrn += cng2ipa[char] + ' '

with open(trnfile + '.ipa', 'w') as f:
    f.write(ipatrn + '\n')
    create_ssml(ipatrn, f)
