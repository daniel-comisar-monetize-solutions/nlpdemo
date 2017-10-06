#!/usr/bin/env python3

# check for nested list: P2096 P2187 P2187 P2188

import bs4
import re
import sqlite3
import sys

if len(sys.argv) != 2:
    exit("Usage: {} <input file>".format(sys.argv[0]))

def has_regex(regex):
    return lambda tag: regex.search(tag.string) if tag.string else False

dtc_regex = re.compile('DTC ([A-Za-z][0-9]{4}).*BMW DTC (\w{6})')
problem_regex = re.compile('Potential problem source')
condition_regex = re.compile('(?:Terminal|Temperature) condition.*')

soup = bs4.BeautifulSoup(open(sys.argv[1], 'r'), 'html.parser')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}
for dtc_node in soup.find_all(has_regex(dtc_regex)):
    (code, bmw_code) = dtc_regex.search(dtc_node.string).groups()
    problem_root = dtc_node.find_next_sibling(has_regex(problem_regex))
    if problem_root:
        cause_list_root = problem_root.find_next_sibling('l')
        if cause_list_root:
            cause_list = [tag.string for tag in cause_list_root.find_all('lbody')]
            condition_index = next((i for i, v in enumerate(cause_list) if condition_regex.search(v)), -1)
            if 0 <= condition_index:
                cause_list[condition_index] = condition_regex.sub('', cause_list[condition_index])
                cause_list = cause_list[:condition_index + 1]
            cause_list = [p.strip() for p in cause_list]
            cur.execute('INSERT OR IGNORE INTO nd_dtc (code, bmw_code) VALUES (?, ?)', (code, bmw_code))
            counts['dtc'] = counts.get('dtc', 0) + cur.rowcount
            for cause in cause_list:
                cur.execute('INSERT OR IGNORE INTO nd_cause (text) VALUES (?)', (cause,))
                counts['cause'] = counts.get('cause', 0) + cur.rowcount
                cur.execute('INSERT OR IGNORE INTO nd_dtc_causes (dtc_id, cause_id) VALUES (?, ?)', (code, cause))
                counts['both'] = counts.get('both', 0) + cur.rowcount
print("{} codes, {} causes, and {} relations added".format(counts.get('dtc', 0), counts.get('cause', 0), counts.get('both', 0)))
conn.commit()
conn.close()
