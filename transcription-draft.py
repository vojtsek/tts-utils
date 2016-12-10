#!/usr/bin/env python3
from unidecode import unidecode
from tts_backers import process_cere

word = input('Type a word:')
word = unidecode(word)
process_cere(word, '.', 'out.wav')

