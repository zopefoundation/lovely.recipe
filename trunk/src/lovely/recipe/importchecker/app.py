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
$Id$
"""
__docformat__ = 'restructuredtext'

import os
import logging

import zc.buildout
import zc.recipe.egg

import pkg_resources

this_loc = pkg_resources.working_set.find(
    pkg_resources.Requirement.parse('lovely.recipe')).location


class ImportChecker(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        logging.getLogger(self.name).info('setting up importchecker')

        requirements, ws = self.egg.working_set()

        path = self.options.get('path', 'src')
        arguments = ['importchecker', path]
        return zc.buildout.easy_install.scripts(
            [('importchecker', 'lovely.recipe.importchecker.importchecker', 'main')],
            ws, self.options['executable'], 'bin',
            extra_paths = [this_loc],
            arguments = arguments,
            )


