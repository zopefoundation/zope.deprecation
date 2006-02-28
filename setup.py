##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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

try:
    from setuptools import setup, Extension, find_packages
    packages = find_packages('src', exclude=['zope.testing'])
    
except ImportException, e:
    from distutils.core import setup, Extension
    packages = ['zope', 'zope.deprecation']
    
setup(name='zope_deprecation',
      version='3.0',

      url='http://svn.zope.org/zope.deprecation',
      license='ZPL 2.1',
      description='Zope 3 Deprecation Infrastructure',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      
      packages=packages,
      package_dir = {'': 'src'},
      namespace_packages=['zope',],

      tests_require = ['zope_testing'],
      include_package_data = True,
      zip_safe = False,
      )
