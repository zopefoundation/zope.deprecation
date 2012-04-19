# used by tests
from . import deprecated

abc = 1

def demo1():
    return 1
deprecated('demo1', 'demo1 is no more.')

def demo2():
    return 2
deprecated('demo2', 'demo2 is no more.')

def demo3():
    return 3
deprecated('demo3', 'demo3 is no more.')

def demo4():
    return 4
def deprecatedemo4():
    """Demonstrate that deprecated() also works in a local scope."""
    deprecated('demo4', 'demo4 is no more.')
