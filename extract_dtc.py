#!/usr/bin/env python3

from extract_utils import cause_start_regex, cause_end_regex, dtc_regex, extract, extract_next, fault_regex, fix_start_regex, fix_end_regex, has_regex
import bs4
import itertools
import sqlite3
import sys

if len(sys.argv) != 2:
    exit('Usage: {} <input file>'.format(sys.argv[0]))

soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}

for dtc_node in soup.find_all(has_regex(dtc_regex)):
    (code, bmw_code, name) = dtc_regex.search(dtc_node.string).groups()
    name = name.strip()
    if not name:
        continue

    fault = extract_next(dtc_node, fault_regex).strip()
    cur.execute('INSERT OR IGNORE INTO nd_dtc (code, bmw_code, name, fault) VALUES (?, ?, ?, ?)', (code, bmw_code, name, fault))
    counts['dtc'] = counts.get('dtc', 0) + cur.rowcount
    counts['dtc_total'] = counts.get('dtc_total', 0) + 1

    for cause in extract(dtc_node, cause_start_regex, cause_end_regex):
        counts['cause_total'] = counts.get('cause_total', 0) + 1
        cur.execute('INSERT OR IGNORE INTO nd_cause (text) VALUES (?)', (cause,))
        counts['cause'] = counts.get('cause', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_cause WHERE text = ?', (cause,))
        cause_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO nd_dtc_causes (dtc_id, cause_id) VALUES (?, ?)', (code, cause_id))
        counts['dtc_cause'] = counts.get('dtc_cause', 0) + cur.rowcount

    for fix in extract(dtc_node, fix_start_regex, fix_end_regex):
        counts['fix_total'] = counts.get('fix_total', 0) + 1
        cur.execute('INSERT OR IGNORE INTO nd_fix (text) VALUES (?)', (fix,))
        counts['fix'] = counts.get('fix', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_fix WHERE text = ?', (fix,))
        fix_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO nd_dtc_fixes (dtc_id, fix_id) VALUES (?, ?)', (code, fix_id))
        counts['dtc_fix'] = counts.get('dtc_fix', 0) + cur.rowcount

print('{} codes, {} causes, {} fixes, {} dtc-cause, and {} dtc-fix relations added'.format(counts.get('dtc', 0), counts.get('cause', 0), counts.get('fix', 0), counts.get('dtc_cause', 0), counts.get('dtc_fix', 0)))
print('{} codes, {} causes, and {} fixes found in total'.format(counts.get('dtc_total', 0), counts.get('cause_total', 0), counts.get('fix_total', 0)))
conn.commit()
conn.close()
