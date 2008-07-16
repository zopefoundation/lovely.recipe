#!/usr/bin/env python2.4
##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Program to extract internationalization markup from Python Code,
Page Templates and ZCML.

This tool will extract all findable message strings from all
internationalizable files in your Zope 3 product. It only extracts message ids
of the specified domain. It defaults to the 'zope' domain and the zope
package.

Note: The Python Code extraction tool does not support domain
      registration, so that all message strings are returned for
      Python code.

Note: The script expects to be executed either from inside the Zope 3 source
      tree or with the Zope 3 source tree on the Python path.  Execution from
      a symlinked directory inside the Zope 3 source tree will not work.

Usage: i18nextract.py [options]
Options:
    -h / --help
        Print this message and exit.
    -d / --domain <domain>
        Specifies the domain that is supposed to be extracted (i.e. 'zope')
    -p / --path <path>
        Specifies the package that is supposed to be searched
        (i.e. 'zope/app')
    -s / --site_zcml <path>
        Specify the location of the 'site.zcml' file. By default the regular
        Zope 3 one is used.
    -e / --exclude-default-domain
        Exclude all messages found as part of the default domain. Messages are
        in this domain, if their domain could not be determined. This usually
        happens in page template snippets.
    -m python-function
        Specify a python function which is added as a maker to the POTMaker.
    -o dir
        Specifies a directory, relative to the package in which to put the
        output translation template.
    -x dir
        Specifies a directory, relative to the package, to exclude.
        May be used more than once.
    --python-only
        Only extract message ids from Python

$Id$
"""

from zope.configuration.name import resolve

import os, sys, getopt
def usage(code, msg=''):
    # Python 2.1 required
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

def app_dir():
    try:
        import zope
    except ImportError:
        # Couldn't import zope, need to add something to the Python path

        # Get the path of the src
        path = os.path.abspath(os.getcwd())
        while not path.endswith('src'):
            parentdir = os.path.dirname(path)
            if path == parentdir:
                # root directory reached
                break
            path = parentdir
        sys.path.insert(0, path)

        try:
            import zope
        except ImportError:
            usage(1, "Make sure the script has been executed "
                     "inside Zope 3 source tree.")

    return os.path.dirname(zope.__file__)

def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hed:s:i:m:p:o:x:',
            ['help', 'domain=', 'site_zcml=', 'path=', 'python-only', 'html'])
    except getopt.error, msg:
        usage(1, msg)

    domain = 'zope'
    path = app_dir()
    include_default_domain = True
    output_dir = None
    exclude_dirs = []
    python_only = False
    extract_html = False
    site_zcml = None
    makers = []
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-d', '--domain'):
            domain = arg
        elif opt in ('-s', '--site_zcml'):
            site_zcml = arg
        elif opt in ('-e', '--exclude-default-domain'):
            include_default_domain = False
        elif opt in ('-m', ):
            makers.append(arg)
        elif opt in ('-o', ):
            output_dir = arg
        elif opt in ('-x', ):
            exclude_dirs.append(arg)
        elif opt in ('--python-only',):
            python_only = True
        elif opt in ('--html',):
            extract_html = True
        elif opt in ('-p', '--path'):
            if not os.path.exists(arg):
                usage(1, 'The specified path does not exist.')
            path = arg
            # We might not have an absolute path passed in.
            if not path == os.path.abspath(path):
                cwd = os.getcwd()
                # This is for symlinks. Thanks to Fred for this trick.
                if os.environ.has_key('PWD'):
                    cwd = os.environ['PWD']
                path = os.path.normpath(os.path.join(cwd, arg))

    # When generating the comments, we will not need the base directory info,
    # since it is specific to everyone's installation
    src_start = path.rfind('src')
    base_dir = path[:src_start]

    output_file = domain+'.pot'
    if output_dir:
        output_dir = os.path.join(path, output_dir)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        output_file = os.path.join(output_dir, output_file)

    print "base path: %r\n" \
          "search path: %s\n" \
          "'site.zcml' location: %s\n" \
          "exclude dirs: %r\n" \
          "domain: %r\n" \
          "include default domain: %r\n" \
          "output file: %r\n" \
          "Python only: %r" \
          "parse html files: %r" \
          % (base_dir, path, site_zcml, exclude_dirs, domain,
             include_default_domain, output_file, python_only, extract_html)

    from zope.app.locales.extract import POTMaker, \
         py_strings, tal_strings, zcml_strings

    maker = POTMaker(output_file, path)
    maker.add(py_strings(path, domain, exclude=exclude_dirs), base_dir)
    if not python_only:
        maker.add(zcml_strings(path, domain, site_zcml), base_dir)
        maker.add(tal_strings(path, domain, include_default_domain,
                              exclude=exclude_dirs), base_dir)
        if extract_html:
            maker.add(tal_strings(path, domain, include_default_domain,
                                  exclude=exclude_dirs, filePattern='*.html'),
                      base_dir)
    for m in makers:
        poMaker = resolve(m)
        maker.add(poMaker(path, base_dir, exclude_dirs))
    maker.write()

if __name__ == '__main__':
    main()
