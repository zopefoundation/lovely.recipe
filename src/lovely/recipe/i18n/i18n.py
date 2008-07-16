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

        package = self.options['package']
        zcml = self.options.get('zcml', None)
        if zcml is None:
            zcml = staticTemplate% package
        else:
            zcml = template % zcml
        partsDir = os.path.join(
                self.buildout['buildout']['parts-directory'],
                self.name,
                )
        if not os.path.exists(partsDir):
            os.mkdir(partsDir)
        zcmlFilename = os.path.join(partsDir, 'configure.zcml')
        file(zcmlFilename, 'w').write(zcml)

        # Generate i18nextract

        arguments = ['%sextract'% self.name,
                     '-d', self.options.get('domain', package),
                     '-s', zcmlFilename,
                     '-p', self.options['location'],
                     '-o', self.options.get('output', 'locales'),
                    ]
        if self.options.get('extract-html', False):
            arguments.append('--html')
        makers = [m for m in self.options.get('maker', '').split() if m!='']
        for m in makers:
            arguments.extend(['-m', m])

        generated = zc.buildout.easy_install.scripts(
            [('%sextract'% self.name, 'lovely.recipe.i18n.i18nextract', 'main')],
            ws, self.options['executable'], 'bin',
            extra_paths = [this_loc],
            arguments = arguments,
            )

        # Generate i18nmergeall

        arguments = ['%smergeall'% self.name,
                     '-l', os.path.join(self.options['location'],
                                        self.options.get('output', 'locales'),
                                       ),
                    ]
        generated.extend(
            zc.buildout.easy_install.scripts(
                [('%smergeall'% self.name,
                  'lovely.recipe.i18n.i18nmergeall',
                  'main')],
                ws, self.options['executable'], 'bin',
                extra_paths = [this_loc],
                arguments = arguments,
            ))

        # Generate i18nstats

        arguments = ['%sstats'% self.name,
                     '-l', os.path.join(self.options['location'],
                                        self.options.get('output', 'locales'),
                                       ),
                    ]
        generated.extend(
            zc.buildout.easy_install.scripts(
                [('%sstats'% self.name,
                  'lovely.recipe.i18n.i18nstats',
                  'main')],
                ws, self.options['executable'], 'bin',
                extra_paths = [this_loc],
                arguments = arguments,
            ))

        return generated


staticTemplate = """<configure xmlns='http://namespaces.zope.org/zope'>
  <include package="%s" />
</configure>
"""


template = """<configure xmlns='http://namespaces.zope.org/zope'
           xmlns:meta="http://namespaces.zope.org/meta"
           >

  %s

</configure>
"""


