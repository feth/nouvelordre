"""
a bizarre test file, not to be ran, just reordered
"""

import a
import b
from c import d

if True:
    from b import e
    import a ; from k import z
    from i.j import k, l, m
    import b.f
    from b import g
    while False:
        from n.o import p ; import y ; import b
        import s
        from a.j import x
        from n.o import q
        import r

exit(1)
exit(5)
exit(7)

def meth():
    import w
    from s.t import u, v
    import a
import w
import a

import w
import a
