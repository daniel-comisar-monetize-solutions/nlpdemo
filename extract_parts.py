#!/usr/bin/env python3

from extract_utils import has_regex
import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

id_regex = re.compile('^Fig\. \d+: Identifying (.*)Courtesy')
soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
count = 0

for id_node in soup.find_all(has_regex(id_regex)):
    if id_node.parent.name == 'caption':
        fig_node = id_node.find_parent('figure')
    else:
        fig_node = id_node.find_previous_sibling('figure')
        if not fig_node and id_node.parent.name == 'div':
            fig_node = id_node.parent.find_previous_sibling('div').find_all('figure')[-1]
    name = id_regex.search(id_node.string).groups(1)[0].strip()
    image = re.sub('^.*_img_', '', fig_node.imagedata['src'])
    cur.execute('INSERT OR IGNORE INTO nd_part (name, image) VALUES (?, ?)', (name, image))
    count += cur.rowcount

print('{} parts inserted'.format(count))
conn.commit()
conn.close()
