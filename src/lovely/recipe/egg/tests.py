##############################################################################
#
# Copyright (c) 2007 Lovely Systems and Contributors.
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
"""
$Id: tests.py 85690 2008-04-24 08:09:41Z jukart $
"""
__docformat__ = 'restructuredtext'

from zc.buildout import testing
import doctest, unittest
from zope.testing import doctest, renormalizing

from lovely.recipe.testing import setUpBuildout


def test_suite():

    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=setUpBuildout,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            tearDown=testing.buildoutTearDown,
            checker=renormalizing.RENormalizing([
                                    testing.normalize_path,
                                    testing.normalize_script,
                                    testing.normalize_egg_py])
            )))

