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
<<<<<<< HEAD
mapfile = 'cng2ipa.tsv'
if len(sys.argv) > 2:
    mapfile = sys.argv[2]
with open(mapfile, 'r') as f:
    for line in f:
        sp = line.strip().split('\t')
        cng2ipa[sp[0]] = sp[1]
=======
with open(sys.argv[2], 'r') as f:
    for line in f:
        sp = line.split('\t')
        cng2ipa[sp[0]] = sp[1].strip()
>>>>>>> 6de27918b42d74c905c67eebf0a5c7c0597fdcbb

trnfile = sys.argv[1]
content = ''
with open(trnfile, 'r') as f:
<<<<<<< HEAD
    content = f.read()
trn = content.split('\n')[0]
for trn in content.split('\n'):
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

    with open(trnfile + '.ipa', 'a') as f:
        f.write(ipatrn + '\n')
    #create_ssml(ipatrn, f)
=======
    for line in f:
        line = line.strip()
        if len(line) < 1:
            continue
        for ph in line.split():
            sys.stdout.write(cng2ipa[ph.strip('012')] + ' ')
        sys.stdout.write('\n')
>>>>>>> 6de27918b42d74c905c67eebf0a5c7c0597fdcbb
