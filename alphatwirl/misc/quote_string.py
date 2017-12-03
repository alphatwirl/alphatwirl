# Tai Sakuma <tai.sakuma@gmail.com>

import re

##__________________________________________________________________||
def quote_string(text):

    if not text: return '""'

    to_quote = False

    if re.search(r'"', text):
        text = re.sub(r'"', r'\"', text) # escape double quote with backslash
        to_quote = True

    if ' ' in text:
        to_quote = True

    if to_quote:
        text = '"{}"'.format(text)

    return text

##__________________________________________________________________||
