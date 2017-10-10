#!/usr/bin/env python3

import os
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
count = 0

for page in range(1, pages + 1):
    text = subprocess.check_output('pdftotext {} -f {} -l {} -'.format(shlex.quote(infile), page, page), shell=True).decode('utf-8')
    blob = textblob.TextBlob(text)
    rows = [(p, filename, page) for p in blob.noun_phrases]
    cur.executemany('INSERT OR IGNORE INTO nd_phrase (text, file, page) values (?, ?, ?)', rows)
    count += cur.rowcount
    conn.commit()

print("{} rows inserted from {} pages".format(count, pages))
conn.close()
