from . import ast
import re
import sys

class ParserError(Exception):
    pass

name_start_char = ':A-Z_a-z\xC0-\xD6\xD8-\xF6\xF8-\u02FF' + \
        '\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF'+\
        '\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD'
name_char = name_start_char + '\-\.0-9' + '\xB7\u0300-\u036F\u203F-\u2040'
name = '[' + name_start_char + '][' + name_char + ']*'

class Parser():
    patterns = {
        'entity': re.compile('<!ENTITY(\s+)(' + name + ')(\s+)(?P<op>["\'])(.*?)(?<!\\\)(?P=op)(\s*)>', re.S|re.U),
        'comment': re.compile('\<!\s*--(.*?)(?:--\s*\>)', re.M|re.S),
    }

    @classmethod
    def parse(cls, text):
        dtd = ast.DTD()
        dtd._struct = []
        cls.split_comments(text, dtd)
        return dtd

    @classmethod
    def split_comments (cls, text, dtd, pointer=0):
        pattern = cls.patterns['comment']
        match = pattern.search(text)
        while match:
            st0 = match.start(0)
            cls.split_entities(text, dtd, pointer=pointer, end=st0)
            comment = ast.Comment(match.group(1))
            dtd.body.append(comment)
            pointer = match.end(0)
            match = pattern.search(text, pointer)
        if len(text) > pointer:
            cls.split_entities(text, dtd, pointer=pointer)

    @classmethod
    def split_entities (cls, text, dtd, pointer=0, end=sys.maxsize):
        pattern = cls.patterns['entity']
        match = pattern.search(text, pointer, end)
        while match:
            st0 = match.start(0)
            dtd._struct.append(text[pointer:st0])
            entity = ast.Entity(match.group(2), match.group(5))
            entity._struct = (match.group(1), match.group(3), match.group(6))
            entity._value_p = match.group(4)
            dtd.body.append(entity)
            pointer = match.end(0)
            match = pattern.search(text, pointer, end)
        if len(text) > pointer:
            dtd._struct.append(text[pointer:end])

