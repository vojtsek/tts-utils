#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# HTTP + URL packages
import httplib2
import wave
import contextlib
import pyaudio
import sys
from urllib.parse import urlencode, quote

CHUNK_SIZE = 1024
MARY_HOST = "localhost"
MARY_PORT = "59125"

def get_duration(fn):
    with contextlib.closing(wave.open(fn, "r")) as f:
        frames = f.getnframes()
        fr = f.getframerate()
        duration = frames / flaot(fr)
        return duration

def send_txt(text):
    query_hash = {"INPUT_TEXT": text,
                  "INPUT_TYPE": "TEXT", 
                  "LOCALE": "en_US",
                  "VOICE": "arctic-hsmm",
                  "OUTPUT_TYPE": "AUDIO",
                  "AUDIO": "WAVE",
                  }
    query = urlencode(query_hash)
    url = "http://{}:{}/process?{}".format(MARY_HOST, MARY_PORT, query)
    h_mary = httplib2.Http()
    resp, content = h_mary.request(url, "POST", query)
    return (resp, content)

def save_wav(resp, content, loc):
    if (resp["content-type"] == "audio/x-wav"):
        with open(loc, "wb") as f:
            f.write(content)
    else:
        raise Exception(content)


def play_wav(wf):
    f = wave.open(wf, "rb")
    pa = pyaudio.PyAudio()
    stream = pa.open(format = pa.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)
    data = f.readframes(CHUNK_SIZE)
    while len(data) > 0:
        stream.write(data)
        data = f.readframes(CHUNK_SIZE)

    stream.stop_stream()
    stream.close()
    pa.terminate()

def main():
    if len(sys.argv) < 2:
        raise Exception("No .txt file provided.")
    # text = "Hi, I am Vojcek."
    loc = "mary.wav"
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            resp, content = send_txt(line)
            try:
                save_wav(resp, content, loc)
                # play_wav(loc)
            except Exception as e:
                print("fuck", e)

if __name__ == "__main__":
    main()
