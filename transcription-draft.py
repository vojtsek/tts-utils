#!/usr/bin/env python3
import sys
import pandas as pd
import subprocess
import logging
from io import StringIO
from unidecode import unidecode
from tts_backers import process_cere

logging.basicConfig(level=logging.INFO)


def ipa_lookup(ipa_map, phoneme):
    # todo: employ information from numbers
    prefix = ''
    stress = phoneme[-1]
    print(stress)
    if stress.isdigit():
        if stress == '1':
            prefix = 'ˈ'
        elif stress == 2:
            prefix = 'ˌ'
        phoneme = phoneme[:-1]
    logging.debug('Looking up "%s"', phoneme)
    print(prefix, phoneme)
    return prefix + ipa_map[ipa_map[0] == phoneme][1].values[0].strip()


def phonemise(model_path, word):
    word = unidecode(word)
    word = word.upper()
    in_fn = 'in.txt'
    with open(in_fn, 'w') as f:
        f.write('{}\n'.format(word))

    proc = subprocess.Popen(['g2p.py', '--model', model_path, '--apply', in_fn], stdout=subprocess.PIPE)
    result = proc.stdout.readline()
    phone_list = result.split()[1:]
    logging.info('Splitted into phonemes: "%s"', str(phone_list))
    return phone_list


def create_phoneme_line_ipa(phoneme, fd):
    fd.write('\t<phoneme alphabet="ipa" ph="{}"> {} </phoneme>\n'.format(phoneme, phoneme))


def create_ssml(phonemes, fd):
        fd.write('<s>\n')
        for ph in phonemes:
            create_phoneme_line_ipa(ph, fd)
        fd.write('</s>\n')


word = input('Type a word:')
ipa_map_path = sys.argv[1]
model_path = sys.argv[2]
ipa_map = pd.read_csv(ipa_map_path, sep='\t', header=None)
phonemes = phonemise(model_path, word)
ipa_phonemes = [ipa_lookup(ipa_map, ph.decode()) for ph in phonemes]
logging.info('Transcribed as: "%s"', "".join(ipa_phonemes))
ph_buffer = StringIO()
create_ssml(ipa_phonemes, ph_buffer)

process_cere(ph_buffer.getvalue(), '.', 'out.wav')
