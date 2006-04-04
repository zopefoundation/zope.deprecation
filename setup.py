##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.deprecation package

$Id$
"""

import os

try:
    from setuptools import setup, Extension, find_packages
    
except ImportError, e:
    from distutils.core import setup, Extension
    
setup(name='zope.deprecation',
      version='3.1.0',

      url='http://svn.zope.org/zope.deprecation/tags/3.1.0',
      license='ZPL 2.1',
      description='Zope 3 Deprecation Infrastructure',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description="This package provides a simple function called "
                       "'deprecated(names, reason)', which Zope3 uses to "
                       "mark APIs and components which will be removed in "
                       "future releases.",
      
      package_dir = {'': os.path.join(os.path.dirname(__file__), 'src')},
      packages=['zope', 'zope.deprecation'],
      namespace_packages=['zope',],

      install_requires=['zope.proxy'],
      tests_require = ['zope.testing'],
      include_package_data = True,
      zip_safe = False,
      )
