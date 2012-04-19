:mod:`zope.deprecation` API
===========================

Deprecating objects inside a module
-----------------------------------

Let's start with a demonstration of deprecating any name inside a module. To
demonstrate the functionality, I have placed the following code inside the
``fixture.py`` file of this package:

.. code-block:: python

  from zope.deprecation import deprecated
  demo1 = 1
  deprecated('demo1', 'demo1 is no more.')

  demo2 = 2
  deprecated('demo2', 'demo2 is no more.')

  demo3 = 3
  deprecated('demo3', 'demo3 is no more.')

The first argument to the ``deprecated()`` function is a list of names that
should be declared deprecated. If the first argument is a string, it is
interpreted as one name. The second argument is the reason the particular name
has been deprecated. It is good practice to also list the version in which the
name will be removed completely.

Let's now see how the deprecation warnings are displayed.

.. doctest::

   >>> import warnings
   >>> from zope.deprecation import fixture
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     fixture.demo1()
   1
   >>> print log[0].category.__name__
   DeprecationWarning
   >>> print log[0].message
   demo1: demo1 is no more.

   >>> import zope.deprecation.fixture
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     zope.deprecation.fixture.demo2()
   2
   >>> print log[0].message
   demo2: demo2 is no more.

You can see that merely importing the affected module or one of its parents
does not cause a deprecation warning. Only when we try to access the name in
the module, we get a deprecation warning. On the other hand, if we import the
name directly, the deprecation warning will be raised immediately.

.. doctest::

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     from zope.deprecation.fixture import demo3
   >>> print log[0].message
   demo3: demo3 is no more.

Deprecation can also happen inside a function.  When we first access
``demo4``, it can be accessed without problems, then we call a
function that sets the deprecation message and we get the message upon
the next access:

.. doctest::

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     fixture.demo4()
   4
   >>> len(log)
   0
   >>> fixture.deprecatedemo4()
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     fixture.demo4()
   4
   >>> print log[0].message.message #XXX oddball case: why nested?
   demo4: demo4 is no more.


Deprecating methods and properties
----------------------------------

New let's see how properties and methods can be deprecated. We are going to
use the same function as before, except that this time, we do not pass in names
as first argument, but the method or attribute itself. The function then
returns a wrapper that sends out a deprecation warning when the attribute or
method is accessed.

.. doctest::

   >>> from zope.deprecation import deprecation
   >>> class MyComponent(object):
   ...     foo = property(lambda self: 1)
   ...     foo = deprecation.deprecated(foo, 'foo is no more.')
   ...
   ...     bar = 2
   ...
   ...     def blah(self):
   ...         return 3
   ...     blah = deprecation.deprecated(blah, 'blah() is no more.')
   ...
   ...     def splat(self):
   ...         return 4
   ...
   ...     @deprecation.deprecate("clap() is no more.")
   ...     def clap(self):
   ...         return 5

And here is the result:

.. doctest::

   >>> my = MyComponent()
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     my.foo
   1
   >>> print log[0].message.message # XXX see above
   foo is no more.
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     my.bar
   2
   >>> len(log)
   0
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     my.blah()
   3
   >>> print log[0].message.message # XXX see above
   blah() is no more.
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     my.splat()
   4
   >>> len(log)
   0
   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     my.clap()
   5
   >>> print log[0].message.message # XXX see above
   clap() is no more.


Deprecating modules
-------------------

It is also possible to deprecate whole modules.  This is useful when
creating module aliases for backward compatibility.  Let's imagine,
the ``zope.deprecation`` module used to be called ``zope.wanda`` and
we'd like to retain backward compatibility:

.. doctest::

   >>> import zope.deprecation
   >>> import sys
   >>> sys.modules['zope.wanda'] = deprecation.deprecated(
   ...     zope.deprecation, 'A module called Wanda is now zope.deprecation.')

Now we can import ``wanda``, but when accessing things from it, we get
our deprecation message as expected:

.. doctest::

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     from zope.wanda import deprecated
   >>> print log[0].message.message # XXX see above
   A module called Wanda is now zope.deprecation.

Before we move on, we should clean up:

.. doctest::

   >>> del deprecated
   >>> del sys.modules['zope.wanda']


Moving modules
--------------

When a module is moved, you often want to support importing from the
old location for a while, generating a deprecation warning when
someone uses the old location.  This can be done using the moved
function.

To see how this works, we'll use a helper function to create two fake
modules in the zope.deprecation package.  First will create a module
in the "old" location that used the moved function to indicate the a
module on the new location should be used:

.. doctest::

   >>> import os
   >>> import tempfile
   >>> tmp_d = tempfile.mkdtemp('deprecation')
   >>> zope.deprecation.__path__.append(tmp_d)
   >>> created_modules = []
   >>> def create_module(modules=(), **kw): #** highlightfail
   ...     modules = dict(modules)
   ...     modules.update(kw)
   ...     for name, src in modules.iteritems():
   ...         pname = name.split('.')
   ...         if pname[-1] == '__init__':
   ...             os.mkdir(os.path.join(tmp_d, *pname[:-1])) #* highlightfail
   ...             name = '.'.join(pname[:-1])
   ...         open(os.path.join(tmp_d, *pname)+'.py', 'w').write(src) #* hf
   ...         created_modules.append(name)
   >>> create_module(old_location=
   ... '''
   ... import zope.deprecation
   ... zope.deprecation.moved('zope.deprecation.new_location', 'version 2')
   ... ''')
  
and we define the module in the new location:

.. doctest::

   >>> create_module(new_location=
   ... '''\
   ... print "new module imported"
   ... x = 42
   ... ''')

Now, if we import the old location, we'll see the output of importing
the old location:

.. doctest::

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     import zope.deprecation.old_location
   new module imported
   >>> print log[0].message.message
   ... # doctest: +NORMALIZE_WHITESPACE
   zope.deprecation.old_location has moved to zope.deprecation.new_location.
   Import of zope.deprecation.old_location will become unsupported
   in version 2
   >>> zope.deprecation.old_location.x
   42

Moving packages
---------------

When moving packages, you need to leave placeholders for each 
module.  Let's look at an example:

.. doctest::

   >>> create_module({
   ... 'new_package.__init__': '''\
   ... print __name__, 'imported'
   ... x=0
   ... ''',
   ... 'new_package.m1': '''\
   ... print __name__, 'imported'
   ... x=1
   ... ''',
   ... 'new_package.m2': '''\
   ... print __name__, 'imported'
   ... def x():
   ...     pass
   ... ''',
   ... 'new_package.m3': '''\
   ... print __name__, 'imported'
   ... x=3
   ... ''',
   ... 'old_package.__init__': '''\
   ... import zope.deprecation
   ... zope.deprecation.moved('zope.deprecation.new_package', 'version 2')
   ... ''',
   ... 'old_package.m1': '''\
   ... import zope.deprecation
   ... zope.deprecation.moved('zope.deprecation.new_package.m1', 'version 2')
   ... ''',
   ... 'old_package.m2': '''\
   ... import zope.deprecation
   ... zope.deprecation.moved('zope.deprecation.new_package.m2', 'version 2')
   ... ''',
   ... })


Now, if we import the old modules, we'll get warnings:

.. doctest::

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     import zope.deprecation.old_package
   zope.deprecation.new_package imported
   >>> print log[0].message
   ... # doctest: +NORMALIZE_WHITESPACE
   zope.deprecation.old_package has moved to zope.deprecation.new_package.
   Import of zope.deprecation.old_package will become unsupported in version 2
   >>> zope.deprecation.old_package.x
   0

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     import zope.deprecation.old_package.m1
   zope.deprecation.new_package.m1 imported
   >>> print log[0].message
   ... # doctest: +NORMALIZE_WHITESPACE
   zope.deprecation.old_package.m1 has moved to zope.deprecation.new_package.m1.
   Import of zope.deprecation.old_package.m1 will become unsupported in
   version 2
   >>> zope.deprecation.old_package.m1.x
   1

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     import zope.deprecation.old_package.m2
   zope.deprecation.new_package.m2 imported
   >>> print log[0].message
   ... # doctest: +NORMALIZE_WHITESPACE
   zope.deprecation.old_package.m2 has moved to zope.deprecation.new_package.m2.
   Import of zope.deprecation.old_package.m2 will become unsupported in
   version 2
   >>> zope.deprecation.old_package.m2.x is zope.deprecation.new_package.m2.x
   True

   >>> (zope.deprecation.old_package.m2.x.func_globals
   ...  is zope.deprecation.new_package.m2.__dict__)
   True

   >>> zope.deprecation.old_package.m2.x.__module__
   'zope.deprecation.new_package.m2'

We'll get an error if we try to import m3, because we didn't create a
placeholder for it:

.. doctest::

   >>> import  zope.deprecation.old_package.m3
   Traceback (most recent call last):
   ...
   ImportError: No module named m3


Before we move on, let's clean up the temporary modules / packages:

.. doctest::

   >>> zope.deprecation.__path__.remove(tmp_d)
   >>> import shutil
   >>> shutil.rmtree(tmp_d)


Temporarily turning off deprecation warnings
--------------------------------------------

In some cases it is desireable to turn off the deprecation warnings for a
short time. To support such a feature, the ``zope.deprecation`` package
provides an attribute called ``__show__``. One can ask for its status by
calling it:

.. doctest::

   >>> from zope.deprecation import __show__
   >>> __show__()
   True

   >>> class Foo(object):
   ...     bar = property(lambda self: 1)
   ...     bar = deprecation.deprecated(bar, 'bar is no more.')
   ...     blah = property(lambda self: 1)
   ...     blah = deprecation.deprecated(blah, 'blah is no more.')
   >>> foo = Foo()

   >>> with warnings.catch_warnings(record=True) as log:
   ...     del warnings.filters[:]
   ...     foo.bar
   1
   >>> print log[0].message
   bar is no more.

You can turn off the depraction warnings using

.. doctest::

   >>> __show__.off()
   >>> __show__()
   False

   >>> foo.blah
   1

Now, you can also nest several turn-offs, so that calling ``off()`` multiple
times is meaningful:

.. doctest::

   >>> __show__.stack
   [False]

   >>> __show__.off()
   >>> __show__.stack
   [False, False]

   >>> __show__.on()
   >>> __show__.stack
   [False]
   >>> __show__()
   False

   >>> __show__.on()
   >>> __show__.stack
   []
   >>> __show__()
   True

You can also reset ``__show__`` to ``True``:

.. doctest::

   >>> __show__.off()
   >>> __show__.off()
   >>> __show__()
   False

   >>> __show__.reset()
   >>> __show__()
   True

Finally, you cannot call ``on()`` without having called ``off()`` before:

.. doctest::

   >>> __show__.on()
   Traceback (most recent call last):
   ...
   IndexError: pop from empty list
