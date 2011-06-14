import pyast

class Node(pyast.Node):
    _abstract = True
    _debug = True

class Entry(Node):
    _abstract = True

class Bundle(Node):
    body = pyast.seq(Entry, null=True)

class Parameter(Entry):
    key = pyast.field(str)
    value = pyast.field(str, null=True)

class Comment(Entry):
    content = pyast.field(str, null=True)

