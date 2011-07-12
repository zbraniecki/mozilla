from . import ast
from itertools import chain, zip_longest

class SerializerError(Exception):
    pass

class Serializer():
    @classmethod
    def serialize(cls, dtd):
        if hasattr(dtd, '_struct'):
            string = ''.join([i for i in chain(*zip_longest(dtd._struct, map(cls.dump_entry, dtd.body))) if i])
        else:
            string = '\n'.join([i for i in map(cls.dump_entry, dtd.body)])
        return string

    @classmethod
    def dump_entry(cls, entry):
        if isinstance(entry, ast.Entity):
            return cls.dump_entity(entry)
        elif isinstance(entry, ast.Comment):
            return cls.dump_comment(entry)
        else:
            raise SerializerError()

    @classmethod
    def dump_entity(cls, entity):
        if not hasattr(entity, '_struct'):
            return '<!ENTITY %s "%s">' % (entity.name, entity.value)
        return '<!ENTITY%s%s%s%s%s%s%s>' % (entity._struct[0],
                                        entity.name,
                                       entity._struct[1],
                                       entity._value_p,
                                       entity.value,
                                       entity._value_p,
                                       entity._struct[2])

    @classmethod
    def dump_comment(cls, comment):
        return '<!--%s-->' % comment.content

