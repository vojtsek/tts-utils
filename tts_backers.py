#!/usr/bin/env python3
import sys
import os
import subprocess
from os.path import join
import pandas as pd


def process_gtts(text, d):
    from gtts import gTTS
    print('processing "{}" with gTTS'.format(text))
    tts = gTTS(text=text, lang='en')
    tts.save(join(d, create_fn(text, 'mp3')))


def process_svox(text, d):
    print('processing "{}" with svox'.format(text))
    try:
        subprocess.call(['pico2wave', '-l', 'en-US', '-w', join(d, create_fn(text)), text])
    except Exception as e:
        print(e)



def process_flite(text, d):
    print('processing "{}" with flite'.format(text))
    with open('tmp.trn', "w") as f:
        f.write(text)
    try:
        subprocess.call(['flite', '-f', 'tmp.trn', '-o', join(d, create_fn(text))])
    except Exception as e:
        print(e)
    finally:
        os.remove('tmp.trn')



def process_cere(text, d, out=None):
    print('processing "{}" with cereproc'.format(text))
    output = out if out is not None else join(d, create_fn(text))
    with open('tmp.trn', "w") as f:
        f.write(text)
    try:
        subprocess.call(['./txt2wav.py', 'tmp.trn', output])
    except Exception as e:
        print(e)
    finally:
        os.remove('tmp.trn')


def process_mary(text, d):
    print('processing "{}" with MaryTTS'.format(text))
    with open('tmp.trn', "w") as f:
        f.write(text)
    try:
        subprocess.call(['./txt2sp.py', 'tmp.trn', join(d, create_fn(text))])
    except Exception as e:
        print(e)
    finally:
        os.remove('tmp.trn')


def create_dir(d):
    if not os.path.isdir(d):
        os.mkdir(d)


def create_fn(text, ext='wav'):
    return '{}.{}'.format(text.replace(' ', '_'), ext)


def process_engine(engine, data, output):
    d = join(output, engine)
    for text in data:
        if engine == 'gtts':
            process_gtts(text, d)
        elif engine == 'svox':
            process_svox(text, d)
        elif engine == 'flite':
            process_flite(text, d)
        elif engine == 'cere':
            process_cere(text, d)
        elif engine == 'mary':
            process_mary(text, d)
        else:
            print('Unknown engine "{}"'.format(engine))
            return


if __name__ == '__main__':
    fn = sys.argv[1]
    output = sys.argv[2]
    engines = sys.argv[3:]
    dataset = pd.read_csv(fn, delimiter=',')
    data = dataset.values[:, 4]
    create_dir(output)
    for eng in engines:
        create_dir(join(output, eng))
        process_engine(eng, data, output)

