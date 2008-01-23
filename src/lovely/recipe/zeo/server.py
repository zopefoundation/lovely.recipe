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

import socket
import cStringIO
import os, shutil
import zc.buildout
import zc.recipe.egg

from lovely.recipe import TemplatedRecipe

from zc.zodbrecipes import StorageServer

class LovelyStorageServer(StorageServer, TemplatedRecipe):

    templatedOptions=['zeo.conf', 'pack']

    def __init__(self, buildout, name, options):
        StorageServer.__init__(self, buildout, name, options)
        self.options['hostname'] = socket.gethostname()
        self.options['__name__'] = self.name
        self.applyIns()

