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
from zc.zope3recipes.recipes import (Instance,
                                     App,
                                     server_types,
                                     event_log2,
                                     this_loc,
                                     site_zcml_template)
from ZConfig.cfgparser import ZConfigParser

class TemplatedInstance:

    templatedOptions = []

    def applyIns(self):
        for option in self.templatedOptions:
            template = self.options.get(option + '.in')
            if template is not None:
                self.options[option] = template % self.options

    def __init__(self, buildout, name, options):
        Instance.__init__(self, buildout, name, options)
        self.options['hostname'] = socket.gethostname()
        self.options['__name__'] = self.name
        template = self.options.get('zope.conf.in')
        if template is not None:
            self.options['zope.conf'] = template % self.options


class LovelyInstance(Instance, TemplatedInstance):

    templatedOptions=['zope.conf', 'zdaemon.conf', 'site.zcml']

    def __init__(self, buildout, name, options):
        Instance.__init__(self, buildout, name, options)
        self.options['hostname'] = socket.gethostname()
        self.options['__name__'] = self.name
        self.applyIns()

    def install(self):
        options = self.options
        run_directory = options['run-directory']
        deployment = self.deployment
        if deployment:
            etc_directory = options['etc-directory']
            site_zcml_path = os.path.join(etc_directory,
                                          self.name+'-site.zcml')
            zope_conf_path = os.path.join(etc_directory,
                                          self.name+'-zope.conf')
            zdaemon_conf_path = os.path.join(etc_directory,
                                             self.name+'-zdaemon.conf')
            event_log_path = os.path.join(options['log-directory'],
                                          self.name+'-z3.log')
            access_log_path = os.path.join(options['log-directory'],
                                           self.name+'-access.log')
            socket_path = os.path.join(run_directory,
                                       self.name+'-zdaemon.sock')
            rc = deployment + '-' + self.name
            creating = [zope_conf_path, zdaemon_conf_path,
                        os.path.join(options['bin-directory'], rc),
                        ]
        else:
            etc_directory = run_directory
            zope_conf_path = os.path.join(etc_directory, 'zope.conf')
            site_zcml_path = os.path.join(etc_directory, 'site.zcml')
            zdaemon_conf_path = os.path.join(etc_directory, 'zdaemon.conf')
            event_log_path = os.path.join(run_directory, 'z3.log')
            access_log_path = os.path.join(run_directory, 'access.log')
            socket_path = os.path.join(run_directory, 'zdaemon.sock')
            rc = self.name
            creating = [run_directory,
                        os.path.join(options['bin-directory'], rc),
                        ]
            if not os.path.exists(run_directory):
                os.mkdir(run_directory)

        try:
            app_loc = options['application-location']

            zope_conf = options.get('zope.conf', '')+'\n'
            zope_conf = ZConfigParse(cStringIO.StringIO(zope_conf))

            if options.get('site.zcml'):
                open(site_zcml_path, 'w').write(
                    site_zcml_template % self.options['site.zcml']
                    )
            else:
                site_zcml_path = os.path.join(app_loc, 'site.zcml')
            zope_conf['site-definition'] = [site_zcml_path]

            server_type = server_types[options['servers']][1]
            for address in options.get('address', '').split():
                zope_conf.sections.append(
                    ZConfigSection('server',
                                   data=dict(type=[server_type],
                                             address=[address],
                                             ),
                                   )
                    )
            if not [s for s in zope_conf.sections
                    if ('server' in s.type)]:
                zope_conf.sections.append(
                    ZConfigSection('server',
                                   data=dict(type=[server_type],
                                             address=['8080'],
                                             ),
                                   )
                    )

            if not [s for s in zope_conf.sections if s.type == 'zodb']:
                raise zc.buildout.UserError(
                    'No database sections have been defined.')

            if not [s for s in zope_conf.sections if s.type == 'accesslog']:
                zope_conf.sections.append(access_log(access_log_path))

            if not [s for s in zope_conf.sections if s.type == 'eventlog']:
                zope_conf.sections.append(event_log('STDOUT'))


            zdaemon_conf = options.get('zdaemon.conf', '')+'\n'
            zdaemon_conf = ZConfigParse(cStringIO.StringIO(zdaemon_conf))

            defaults = {
                'program': "%s -C %s" % (os.path.join(app_loc, 'runzope'),
                                         zope_conf_path,
                                         ),
                'daemon': 'on',
                'transcript': event_log_path,
                'socket-name': socket_path,
                'directory' : run_directory,
                }
            if deployment:
                defaults['user'] = options['user']
            runner = [s for s in zdaemon_conf.sections
                      if s.type == 'runner']
            if runner:
                runner = runner[0]
            else:
                runner = ZConfigSection('runner')
                zdaemon_conf.sections.insert(0, runner)
            for name, value in defaults.items():
                if name not in runner:
                    runner.addValue(name, value)

            if not [s for s in zdaemon_conf.sections
                    if s.type == 'eventlog']:
                # No database, specify a default one
                zdaemon_conf.sections.append(event_log2(event_log_path))

            zdaemon_conf = str(zdaemon_conf)

            self.egg.install()
            requirements, ws = self.egg.working_set()

            open(zope_conf_path, 'w').write(str(zope_conf))
            open(zdaemon_conf_path, 'w').write(str(zdaemon_conf))

            zc.buildout.easy_install.scripts(
                [(rc, 'zc.zope3recipes.ctl', 'main')],
                ws, options['executable'], options['bin-directory'],
                extra_paths = [this_loc],
                arguments = ('['
                             '\n        %r,'
                             '\n        %r,'
                             '\n        %r, %r,'
                             '\n        ]+sys.argv[1:]'
                             '\n        '
                             % (os.path.join(app_loc, 'debugzope'),
                                zope_conf_path,
                                '-C', zdaemon_conf_path,
                                )
                             ),
                )

            return creating

        except:
            for f in creating:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                elif os.path.exists(f):
                    os.remove(f)
            raise


    update = install

class LovelyApp(App, TemplatedInstance):

    templatedOptions=['site.zcml']

    def __init__(self, buildout, name, options):
        App.__init__(self, buildout, name, options)
        self.options['hostname'] = socket.gethostname()
        self.options['__name__'] = self.name
        self.applyIns()
