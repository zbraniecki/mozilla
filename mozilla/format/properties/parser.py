from . import ast
import re
import string

class ParserError(Exception):
    pass

class Parser():
    patterns = {
        'id': re.compile('^[\'"]?(\w+)[\'"]?'),
        'value': re.compile('^(?P<op>[\'"])(.*?)(?<!\\\)(?P=op)'),
    }

    def parse(self, text):
        self.content = text
        bundle = ast.Bundle()
        while len(self.content):
            bundle.body.append(self.get_entry())
            self.get_ws()
        return bundle

    def get_ws(self):
        content = self.content.lstrip()
        ws = self.content[:len(content)*-1]
        self.content = content
        return ws

    def get_entry(self):
        if self.content[:8] == '<!ENTITY':
            return self.get_entity()
        elif self.content[:4] == '<!--':
            return self.get_comment()
        else:
            print(self.content[:10])
            raise ParserError()
        return ast.Entity('id', 'name')

    def get_entity(self):
        self.content = self.content[8:]
        self.get_ws()
        ptr = 0
        while self.content[ptr] not in string.whitespace:
            ptr += 1
        name = self.content[:ptr]
        self.content = self.content[ptr:]
        self.get_ws()
        value = self.get_value()
        self.get_ws()
        self.content = self.content[1:]
        return ast.Entity(name, value)

    def get_value(self):
        match = self.patterns['value'].match(self.content)
        if not match:
            raise ParserError()
        self.content = self.content[match.end(0):]
        return match.group(1)
