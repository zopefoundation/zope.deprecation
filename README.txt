****************
zope.deprecation
****************

When we started working on Zope 3.1, we noticed that the hardest part of the
development process was to ensure backward-compatibility and correctly mark
deprecated modules, classes, functions, methods and properties. This package
provides a simple function called 'deprecated(names, reason)' to deprecate the
previously mentioned Python objects.

Releases
********

==================
3.4.1 (unreleased)
==================

Added support to bootstrap on Jython.

Fix zope.deprecation.warn() to make the signature identical to
warnings.warn() and to check for *.pyc and *.pyo files.

==================
3.4.0 (2007/07/19)
==================

Release 3.4 final, corresponding to Zope 3.4.

==================
3.3.0 (2007/02/18)
==================

Corresponds to the verison of the zope.deprecation package shipped as part of
the Zope 3.3.0 release.

====================
3.2.0.2 (2006/04/15)
====================

Fix packaging bug:  'package_dir' must be a *relative* path.

==================
3.2.0 (2006/01/05)
==================

Corresponds to the verison of the zope.deprecation package shipped as part of
the Zope 3.2.0 release.

Refactored to eliminate dependency on 'zope.proxy'. This was an especially
bad dependency due to the required C exension in 'zope.proxy'.

==================
3.1.0 (2005/10/03)
==================

Corresponds to the verison of the zope.deprecation package shipped as part of
the Zope 3.1.0 release.
