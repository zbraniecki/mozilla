from . import ast
import re
import string
import sys

class ParserError(Exception):
    pass

class Parser():
    patterns = {
        'entity': re.compile('^([ \t]*)([^#!\s\n][^=:\n]*?)([ \t]*)[:=]([ \t]*)(.*?)(?<!\\\)(?=\n|\Z|\r)',re.S|re.M),
        'comment': re.compile('^(#[^\n]*\n?)+',re.M|re.S),
    }


    @classmethod
    def parse(cls, text):
        bundle = ast.Bundle()
        bundle._struct = []
        cls.split_comments(text, bundle, struct=True)
        return bundle

    # problem with commented out entities
    @classmethod
    def parse_to_entitylist(cls, text):
        entitylist = EntityList(None)
        text = cls.patterns['comment'].sub('', text)
        matchlist = cls.patterns['entity'].findall(text)
        for match in matchlist:
            entitylist.add(Entity(match[0], match[1]))
        return entitylist
    
    @classmethod
    def parse_entity(cls, text, code='default'):
        match = self.patterns['entity'].match(text)
        if not match:
            raise Exception()
        entity = Entity(match.group(1))
        entity.set_value(match.group(2), code=code)
        return entity

    @classmethod
    def split_comments(cls, text, bundle, pointer=0, struct=True):
        pattern = cls.patterns['comment']
        match = pattern.search(text, pointer)
        while match:
            st0 = match.start(0)
            cls.split_parameters(text, bundle, pointer=pointer, end=st0, struct=struct)
            comment = ast.Comment(match.group(0)[1:].replace('\n#','\n'))
            bundle.body.append(comment)
            pointer = match.end(0)
            match = pattern.search(text, pointer)
        if len(text) > pointer:
            cls.split_parameters(text, bundle, pointer=pointer, struct=struct)

    @classmethod
    def split_parameters(cls, text, bundle, pointer=0, end=sys.maxsize, struct=True):
        pattern = cls.patterns['entity']
        match = pattern.search(text, pointer, end)
        while match:
            st0 = match.start(0)
            if struct:
                bundle._struct.append(text[pointer:st0])
            groups = match.groups()
            param = ast.Parameter(groups[1], groups[4])
            if struct:
                param._struct = (groups[0], groups[2], groups[3])
                param._value_p = match.start(2)-st0
            bundle.body.append(param)
            pointer = match.end(0)
            match = pattern.search(text, pointer, end)
        if struct and len(text) > pointer:
            bundle._struct.append(text[pointer:end])
