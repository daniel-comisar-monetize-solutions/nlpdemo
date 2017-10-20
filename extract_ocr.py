#!/usr/bin/env python3

from extract_utils import dtc_regex, trim_regex
import json
import re
import sqlite3
import sys

class Lines():
    def __init__(self, lines):
        self.lines = lines
    def pop(self, regex=None):
        while True:
            if not self.lines:
                return None
            next_line = self.lines[0]
            self.lines = self.lines[1:]
            if not regex or regex.search(next_line):
                return next_line
    def pop_after(self, regex):
        while True:
            next_line = self.pop()
            if not next_line:
                return None
            if regex.search(next_line):
                return self.pop()
    def pop_until(self, regex):
        result = []
        while True:
            next_line = self.pop()
            if not next_line or regex.search(next_line):
                return result
            result.append(next_line)

if len(sys.argv) != 3:
    exit('Usage: {} <input file> <input file>'.format(sys.argv[0]))

action_regex = re.compile('Action in service')
cause_regex = re.compile('Potential problem source')
condition_regex = re.compile('(?:Terminal|Temperature) condition.*')
fault_regex = re.compile('Fault (?:description|effect and breakdown warning)')

text = json.loads(open(sys.argv[1], 'r').read())['fullTextAnnotation']['text']
text += json.loads(open(sys.argv[2], 'r').read())['fullTextAnnotation']['text']
lines = Lines(text.split('\n'))
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
counts = {}

while True:
    dtc_line = lines.pop(dtc_regex)
    if not dtc_line:
        break
    (code, bmw_code, name) = dtc_regex.search(dtc_line).groups()
    name = name.strip()
    if not name:
        continue

    fault = lines.pop_after(fault_regex)
    if not fault:
        continue
    cur.execute('INSERT OR IGNORE INTO nd_dtc (code, bmw_code, name, fault) VALUES (?, ?, ?, ?)', (code, bmw_code, name, fault))
    counts['dtc'] = counts.get('dtc', 0) + cur.rowcount

    lines.pop(cause_regex)
    for cause in lines.pop_until(condition_regex):
        cause = trim_regex.sub('', cause)
        cur.execute('INSERT OR IGNORE INTO nd_cause (text) VALUES (?)', (cause,))
        counts['cause'] = counts.get('cause', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_cause WHERE text = ?', (cause,))
        cause_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO nd_dtc_causes (dtc_id, cause_id) VALUES (?, ?)', (code, cause_id))
        counts['dtc_cause'] = counts.get('dtc_cause', 0) + cur.rowcount

    lines.pop(action_regex)
    for fix in lines.pop_until(fault_regex):
        fix = trim_regex.sub('', fix)
        cur.execute('INSERT OR IGNORE INTO nd_fix (text) VALUES (?)', (fix,))
        counts['fix'] = counts.get('fix', 0) + cur.rowcount
        cur.execute('SELECT id FROM nd_fix WHERE text = ?', (fix,))
        fix_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO nd_dtc_fixes (dtc_id, fix_id) VALUES (?, ?)', (code, fix_id))
        counts['dtc_fix'] = counts.get('dtc_fix', 0) + cur.rowcount

print('{} codes, {} causes, {} fixes, {} dtc-cause relations, and {} dtc-fix relations added'.format(counts.get('dtc', 0), counts.get('cause', 0), counts.get('fixes', 0), counts.get('dtc_cause', 0), counts.get('dtc_fix', 0)))
conn.commit()
conn.close()
