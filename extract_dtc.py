#!/usr/bin/env python3

from extract_utils import dtc_regex, extract, has_regex
import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

cause_regex = re.compile('Potential problem source')
condition_regex = re.compile('(?:Terminal|Temperature) condition.*')
fault_regex = re.compile('Fault description')
soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}

for dtc_node in soup.find_all(has_regex(dtc_regex)):
    (code, bmw_code, name) = dtc_regex.search(dtc_node.string).groups()

    name = name.strip()
    if not name:
        continue

    fault_root = dtc_node.find_next_sibling(has_regex(fault_regex))
    if not fault_root:
        fault_root = dtc_node.parent.find_next_sibling('div').find(has_regex(fault_regex))
    fault = fault_root.find_next_sibling('p').string.strip()

    cause_root = dtc_node.find_next_sibling(has_regex(cause_regex))
    if not cause_root:
        cause_root = dtc_node.parent.find_next_sibling('div').find(has_regex(cause_regex))

    cause_list = extract(cause_root, condition_regex)
    cur.execute('INSERT OR IGNORE INTO nd_dtc (code, bmw_code, name, fault) VALUES (?, ?, ?, ?)', (code, bmw_code, name, fault))
    counts['dtc'] = counts.get('dtc', 0) + cur.rowcount
    for cause in cause_list:
        cur.execute('INSERT OR IGNORE INTO nd_cause (text) VALUES (?)', (cause,))
        counts['cause'] = counts.get('cause', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_cause WHERE text = ?', (cause,))
        cause_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO nd_dtc_causes (dtc_id, cause_id) VALUES (?, ?)', (code, cause_id))
        counts['both'] = counts.get('both', 0) + cur.rowcount

print('{} codes, {} causes, and {} relations added'.format(counts.get('dtc', 0), counts.get('cause', 0), counts.get('both', 0)))
conn.commit()
conn.close()
