#!/usr/bin/env python3

from extract_utils import dtc_regex, extract, has_regex
import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

action_regex = re.compile('Action in service')
fault_regex = re.compile('Fault effect and breakdown warning')
soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}

for dtc_node in soup.find_all(has_regex(dtc_regex)):
    (code, bmw_code) = dtc_regex.search(dtc_node.string).groups()
    fix_root = dtc_node.find_next_sibling(has_regex(action_regex))
    if not fix_root:
        fix_root = dtc_node.parent.find_next_sibling('div').find(has_regex(action_regex))
        if not fix_root:
            continue

    fix_list = extract(fix_root, fault_regex)
    cur.execute('INSERT OR IGNORE INTO nd_dtc (code, bmw_code) VALUES (?, ?)', (code, bmw_code))
    counts['dtc'] = counts.get('dtc', 0) + cur.rowcount
    for fix in fix_list:
        cur.execute('INSERT OR IGNORE INTO nd_fix (text) VALUES (?)', (fix,))
        counts['fix'] = counts.get('fix', 0) + cur.rowcount
        cur.execute('INSERT OR IGNORE INTO nd_dtc_fixes (dtc_id, fix_id) VALUES (?, ?)', (code, fix))
        counts['both'] = counts.get('both', 0) + cur.rowcount

print('{} codes, {} fixes, and {} relations added'.format(counts.get('dtc', 0), counts.get('fix', 0), counts.get('both', 0)))
conn.commit()
conn.close()