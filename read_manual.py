#!/usr/bin/env python3

import os
import shlex
import sqlite3
import subprocess
import sys
import textblob

if len(sys.argv) == 1:
    exit('Missing argument: input file location')
infile = sys.argv[1]
filename = os.path.basename(sys.argv[1])
pages = int(subprocess.check_output('pdfinfo {} | grep Pages: | awk \'{{print $2}}\''.format(shlex.quote(infile)), shell=True))
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
# cur.execute('CREATE TABLE IF NOT EXISTS phrases (phrase text, file text, page int, unique(phrase, file, page))')
count = 0
for page in range(1, pages + 1):
    text = subprocess.check_output('pdftotext {} -f {} -l {} -'.format(shlex.quote(infile), page, page), shell=True).decode('utf-8')
    blob = textblob.TextBlob(text)
    rows = [(p, filename, page) for p in blob.noun_phrases]
    cur.executemany('INSERT OR IGNORE INTO nd_phrase (text, file, page) values (?, ?, ?)', rows)
    count += cur.rowcount
print("{} rows inserted".format(count))
conn.commit()
conn.close()
