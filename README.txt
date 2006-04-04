zope.deprecation Package Readme
===============================

Overview
--------

When we started working on Zope 3.1, we noticed that the hardest part of the
development process was to ensure backward-compatibility and correctly mark
deprecated modules, classes, functions, methods and properties. This package
provides a simple function called 'deprecated(names, reason)' to deprecate the
previously mentioned Python objects.

Changes
-------

See CHANGES.txt.

Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.deprecation/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.deprecation/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.deprecation/trunk

- Note that the 'src/zope/deprecation' package is acutally a 'svn:externals'
  link to the corresponding package in the Zope3 trunk (or to a specific tag,
  for released versions of the package).
