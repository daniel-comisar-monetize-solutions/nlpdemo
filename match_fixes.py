#!/usr/bin/env python3

import Levenshtein
import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

refs = {}
for (code, text) in cur.execute('SELECT * FROM nd_referencefix'):
    refs[text] = code

for (text,) in cur.execute('SELECT * FROM nd_fix'):
    max_score = -1
    max_ref = ''
    for ref in refs:
        score = Levenshtein.seqratio(text.split(), ref.split())
        if max_score < score:
            max_score = score
            max_ref = ref

    print('Manual text: {}'.format(text))
    print('Refer. text: {}'.format(max_ref))
    print('Similarity:  {}'.format(max_score))
    print()

conn.commit()
conn.close()
