import re

dtc_regex = re.compile('DTC ([A-Za-z][0-9]{4,5}).*BMW DTC (\w{6})')

def has_regex(regex):
    return lambda tag: regex.search(tag.string) if tag.string else False

def extract(root, end_regex):
    trim_regex = re.compile('(^[○\s]*)|([.\s]*$)')
    def fix(result, last):
        remainder = trim_regex.sub('', end_regex.sub('', last))
        return result + [remainder] if remainder else result

    result = []
    for tag in list(root.next_siblings) + root.parent.find_next_sibling('div').contents:
        if tag.name == 'p' and tag.string and tag.string != '\n':
            if end_regex.search(tag.string):
                return fix(result, tag.string)
            result.append(trim_regex.sub('', tag.string))
        elif tag.name == 'l':
            for l in tag.find_all('lbody'):
                if end_regex.search(l.string):
                    return fix(result, l.string)
                result.append(trim_regex.sub('', l.string))
    raise Exception('Failed to find terminating string')
