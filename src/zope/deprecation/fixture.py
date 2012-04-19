# used by tests
from . import deprecated

abc = 1

def demo1(): #pragma NO COVER  (used only in doctests)
    return 1
deprecated('demo1', 'demo1 is no more.')

def demo2(): #pragma NO COVER  (used only in doctests)
    return 2
deprecated('demo2', 'demo2 is no more.')

def demo3(): #pragma NO COVER  (used only in doctests)
    return 3
deprecated('demo3', 'demo3 is no more.')

def demo4(): #pragma NO COVER  (used only in doctests)
    return 4
def deprecatedemo4(): #pragma NO COVER  (used only in doctests)
    """Demonstrate that deprecated() also works in a local scope."""
    deprecated('demo4', 'demo4 is no more.')
