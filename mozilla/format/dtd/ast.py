import pyast

class Node(pyast.Node):
    _abstract = True
    _debug = True

class Entry(Node):
    _abstract = True

class DTD(Node):
    body = pyast.seq(Entry, null=True)

class Entity(Entry):
    name = pyast.field(str)
    value = pyast.field(str, null=True)

class Comment(Entry):
    content = pyast.field(str, null=True)

