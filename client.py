#! /usr/bin/env python3
import requests
import subprocess
import time
import json
import os
import sys
import argparse

def make_post_request(endpoint, data={}, files={}, headers={'Accept': 'application/json'}):
    API_URL = 'http://89.190.54.121:5710'
    r = requests.post('{}/{}'.format(API_URL, endpoint), headers=headers, data=data, files=files)
    print(r.status_code)
    if r.status_code == 201 or r.status_code == 200:
        return r
    else:
        return None

def record_wav(wfn, rate='16000', channels=1, length=1000):
    if os.path.exists(wfn):
        os.remove(wfn)
    # todo spawn in new thread and send kill after length
    subprocess.call(['rec', '-r', rate, '-c', channels, wfn])

def synthesize(ssmlfile, ofile):
    subprocess.call(['./txt2wav.py', ssmlfile, ofile])

def play(f):
    subprocess.call(['play', f])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--recording', default='', help='recording to process')
    parser.add_argument('--transcriptions', default='', help='transcription to process directly')
    parser.add_argument('--nbest', default='3', help='transcription to process directly')
    parser.add_argument('--word_confidence', action='store_true', help='transcription to process directly')
    args = parser.parse_args()
    wavfile = args.recording
    nbest = args.nbest
    word_confidence = args.word_confidence
    trns = args.transcriptions
    if wavfile == '' and trns == '':
        wavfile = 'rec.wav'
        record_wav(wavfile)
    ssmlfile = 'in.ssml'
    ofile = 'synth.wav'
    if trns == '':
        body = {'n': nbest}
        if word_confidence:
            body['wc'] = 'true'
        r = make_post_request('transcribe', body, {'wavfile': open(wavfile, 'rb')}, '')
        if r == None:
            print('Server error occured')
            sys.exit(1)
        trns = r.json()
    else:
        jf = open(trns, 'r')
        trns = json.load(jf)

    def str2lst(s):
        res = map(lambda x: float(x.strip().strip('[]')), s.split(','))
        return list(res)

    if word_confidence:
        key_f = lambda x: str2lst(x['confidence'])[-1]
    else:
        key_f = lambda x: float(x['confidence'])
    trns = sorted(trns, key=key_f, reverse=True)
    for trn in trns:
        print(trn)
        r = make_post_request('synthesize', {'trn': trn['transcription']})
        with open(ofile, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        play(ofile)
