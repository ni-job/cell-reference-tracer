from graphviz import Digraph


def init_digraph():
    val = Digraph()
    val.clear(keep_attrs=False)
    val.attr(
        'node',
        color='lightblue2',
        style='filled',
        shape='record',
        fontname='MS Gothic'
    )
    return val
