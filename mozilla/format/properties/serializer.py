#from ...core import paramList, param, Comment
from . import ast
import re
from itertools import chain, zip_longest

class Serializer():
    @classmethod
    def serialize(cls, prop):
        if hasattr(prop, '_struct'):
            string = ''.join([i for i in 
                              chain(*zip_longest(
                                  prop._struct, 
                                  map(cls.dump_entry, prop.body))) if i])
        else:
            string = '\n'.join([cls.dump_entry(element) for element in prop.body])
        return string

    @classmethod
    def dump_entry(cls, element, fallback=None):
        if isinstance(element, ast.Parameter):
            return cls.dump_parameter(element)
        elif isinstance(element, ast.Comment):
            return cls.dump_comment(element)
        else:
            return element

    @classmethod
    def dump_parameter(cls, param):
        if False and hasattr(param, '_struct'):
            match = Parser.patterns['param'].match(param.params['source']['string'])
            string = param.params['source']['string'][0:match.start(1)]
            string += param.id
            string += param.params['source']['string'][match.end(1):match.start(2)]
            string += param.value
            string += param.params['source']['string'][match.end(2):]
        else:
            string = '%s = %s' % (param.key, param.value)
        return string

    @classmethod
    def dump_paramlist(cls, elist):
        string = ''.join([cls.dump_param(param)+'\n' for param in elist.values()])
        return string

    @classmethod
    def dump_comment (cls, comment):
        string = comment.content
        if string:
            pattern = re.compile('\n')
            string = pattern.sub('\n#', string)
            string = '#' + string
            if string.endswith('#'):
                string = string[:-1]
        return string

