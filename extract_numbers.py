#!/usr/bin/env python3

from extract_utils import has_regex, id_regex
import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

blank_regex = re.compile('^\s*$')
number_regex = re.compile('\s*(\(\d+\))\s*')
soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
count = 0

for num_node in soup.find_all(has_regex(number_regex)):
    numbers = re.findall(number_regex, num_node.text)
    text = number_regex.sub(' ', num_node.text).strip()
    if blank_regex.search(text):
        continue

    id_node = num_node
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

    for num in numbers:
        cur.execute('INSERT OR IGNORE INTO nd_partlabel (label, text, part_id) VALUES (?, ?, ?)', (num, text, part_id))
        count += cur.rowcount

print('{} labels inserted'.format(count))
conn.commit()
conn.close()
