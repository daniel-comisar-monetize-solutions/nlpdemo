#!/usr/bin/env python3

import os
import re
import shlex
import sqlite3
import subprocess
import sys
import textblob

if len(sys.argv) not in [2, 3]:
    exit('Usage: {} <input file> <max pages (optional)>'.format(sys.argv[0]))

infile = sys.argv[1]
filename = os.path.basename(sys.argv[1])
pages = int(subprocess.check_output('pdfinfo {} | grep Pages: | awk \'{{print $2}}\''.format(shlex.quote(infile)), shell=True))
pages = min(pages, int(sys.argv[2])) if 2 < len(sys.argv) else pages
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}
phrases = {}

for page in range(1, pages + 1):
    text = subprocess.check_output('pdftotext {} -f {} -l {} -'.format(shlex.quote(infile), page, page), shell=True).decode('utf-8')
    blob = textblob.TextBlob(text)
    for p in blob.noun_phrases:
        phrases[p] = phrases.get(p, 0) + 1

for p in phrases:
    cur.execute('INSERT OR IGNORE INTO nd_phrase (text, count) VALUES (?, ?)', (p, phrases[p]))
    counts['phrase'] = counts.get('phrase', 0) + cur.rowcount

for page in range(1, pages + 1):
    text = subprocess.check_output('pdftotext {} -f {} -l {} -'.format(shlex.quote(infile), page, page), shell=True).decode('utf-8')
    blob = textblob.TextBlob(text)
    for s in blob.sentences:
        cur.execute('INSERT OR IGNORE INTO nd_sentence (text, page, filename) VALUES (?, ?, ?)', (s.raw, page, filename))
        counts['sentence'] = counts.get('sentence', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_sentence WHERE text = ?', (s.raw,))
        sentence_id = cur.fetchone()[0]
        for p in s.noun_phrases:
            cur.execute('SELECT id FROM nd_phrase WHERE text = ?', (p,))
            phrase_id = cur.fetchone()[0]
            cur.execute('INSERT OR IGNORE INTO nd_phrase_sentences (phrase_id, sentence_id) VALUES (?, ?)', (phrase_id, sentence_id))
            counts['relation'] = counts.get('relation', 0) + cur.rowcount

print("{} phrases, {} sentences, and {} relations inserted".format(counts.get('phrase', 0), counts.get('sentence', 0), counts.get('relation', 0)))
conn.commit()
conn.close()
