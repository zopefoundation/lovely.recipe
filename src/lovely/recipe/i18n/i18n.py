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


class I18n(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.options['eggs'] =   self.options['eggs'] + '\n' \
                               + 'zope.app.locales' + '\n' \
                               + self.options['package']
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        logging.getLogger(self.name).info('setting up i18n tools')

        requirements, ws = self.egg.working_set()

        arguments = ['i18nextract',
                     '-d', self.options.get('domain',
                                            self.options['package']),
                     '-p', self.options['location'],
                     '-o', self.options.get('output', 'locales'),
                    ]
        zcml = self.options('zcml', None)
        if zcml is not None:
             arguments.extend(['-s', self.options['zcml'],])
        makers = [m for m in self.options.get('maker', '').split() if m!='']
        for m in makers:
            arguments.extend(['-m', m])
        generated = zc.buildout.easy_install.scripts(
            [('i18nextract', 'lovely.recipe.i18n.i18nextract', 'main')],
            ws, self.options['executable'], 'bin',
            extra_paths = [this_loc],
            arguments = arguments,
            )

        arguments = ['i18nmergeall',
                     '-l', os.path.join(self.options['location'],
                                        self.options.get('output', 'locales'),
                                       ),
                    ]
        generated.extend(
            zc.buildout.easy_install.scripts(
                [('i18nmergeall', 'lovely.recipe.i18n.i18nmergeall', 'main')],
                ws, self.options['executable'], 'bin',
                extra_paths = [this_loc],
                arguments = arguments,
            ))

        return generated


