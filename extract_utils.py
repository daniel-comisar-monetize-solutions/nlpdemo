import collections
import itertools
import re

cause_end_regex = re.compile('(?:Terminal|Temperature) condition.*')
cause_start_regex = re.compile('Potential problem source')
dtc_regex = re.compile('DTC (\w{5}).*BMW DTC (\w{6}):?((?:(?!Information).)*)')
fault_regex = re.compile('Fault description')
fix_end_regex = re.compile('Fault effect and breakdown warning')
fix_start_regex = re.compile('Action in service')
id_regex = re.compile('^Fig\. \d+: Identifying ((?:(?!Courtesy).)*)')
trim_regex = re.compile('(^[○o\s]*)|([.\s]*$)')

def consume(iterator):
    collections.deque(iterator, maxlen=0)

def consume_until(predicate, iterator):
    consume(itertools.takewhile(lambda x: not predicate(x), iterator))

def extract(root_node, start_regex, end_regex):
    root_iterator = trim_iterator(text_iterator(sibling_iterator(root_node)))
    consume_until(lambda x: start_regex.search(x), root_iterator)
    return takewhile_plusone(lambda x: not end_regex.search(x), root_iterator, fix_last(end_regex))

def extract_next(root_node, regex):
    iterator = text_iterator(sibling_iterator(root_node))
    consume_until(lambda x: regex.search(x), iterator)
    return next(iterator).strip()

def fix_last(regex):
    def fix(x):
        remainder = trim_regex.sub('', regex.sub('', x))
        if not remainder:
            raise StopIteration
        return remainder
    return fix

def has_regex(regex):
    return lambda tag: regex.search(tag.string) if tag.string else False

def sibling_iterator(node):
    while node:
        yield node
        if node.next_sibling:
            node = node.next_sibling
        else:
            node = node.parent.find_next_sibling('div').find()

def takewhile_plusone(predicate, iterator, process_last=lambda x: x):
    for x in iterator:
        if predicate(x):
            yield x
        else:
            yield process_last(x)
            break

def text_iterator(node_iter):
    for node in node_iter:
        if node.name == 'p' and node.string and node.string != '\n':
            yield node.string
        elif node.name == 'l':
            for l in node.find_all('lbody'):
                yield l.string

def trim_iterator(text_iter):
    for text in text_iter:
        trimmed = trim_regex.sub('', text)
        if trimmed:
            yield trimmed
