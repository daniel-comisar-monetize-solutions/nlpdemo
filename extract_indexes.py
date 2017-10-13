#!/usr/bin/env python3

from extract_utils import has_regex, id_regex
import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

explain_regex = re.compile('^Explanation$')
label_regex = re.compile('^\w\d*$')
soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
count = 0

for explain_node in soup.find_all(has_regex(explain_regex)):
    if explain_node.name != 'text':
        continue

    id_node = explain_node
    while not id_node.text or not id_regex.search(id_node.text):
        prev_node = id_node.find_previous_sibling('text')
        if not prev_node:
            prev_page = id_node.find_parent('page').find_previous_sibling('page')
            prev_node = next(iter(prev_page.find_all('text')[-1:]), None)
        id_node = prev_node
    name = id_regex.search(id_node.text).groups(1)[0].strip()

    cur.execute('SELECT ID FROM nd_part WHERE NAME = ?', (name,))
    part_id = cur.fetchone()
    if not part_id:
        continue
    part_id = part_id[0]

    next_label = explain_node.find_next_sibling('text')
    while next_label and next_label.string and label_regex.search(next_label.string):
        next_text = next_label.find_next_sibling('text')
        cur.execute('INSERT OR IGNORE INTO nd_partlabel (label, text, part_id) VALUES (?, ?, ?)', (next_label.string, next_text.string, part_id))
        count += cur.rowcount
        next_label = next_text.find_next_sibling('text')

print('{} labels inserted'.format(count))
conn.commit()
conn.close()
