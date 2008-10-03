=======================
Egg Box Buildout Recipe
=======================

This recipe is derivd from zc.recipe.egg, but instead of just creating
paths, it generates a directory structure for each top-level
namespace. It is also possible to automatically zip the generated
directories which is espacially usefull if used in Google Appengine
environments. The recipies path option is filled with the created path
so it can be referenced by other buildout sections which may want to
use the recipe.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = packages
    ... find-links = http://download.zope.org/distribution
    ...
    ... [packages]
    ... recipe = lovely.recipe:eggbox
    ... eggs = zope.dublincore
    ...        zope.formlib
    ...        pytz
    ... """)
    >>> print system(buildout),
    Installing packages.

We now have a zip file for each top-level directory. Note that the
zip-files are ending with .egg for pkg_resources compatibility.

    >>> ls(sample_buildout + '/parts/packages')
    -  BTrees.egg
    -  RestrictedPython.egg
    -  ThreadedAsync.egg
    -  ZConfig.egg
    -  ZEO.egg
    -  ZODB.egg
    -  ZopeUndo.egg
    -  persistent.egg
    -  pytz.egg
    -  transaction.egg
    -  zdaemon.egg
    -  zodbcode.egg
    -  zope.egg

It is possible to disable zipping. And also to exclude or include
patterns of files. So for example we can strip down pytz. We can also
create a script.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = packages test
    ... find-links = http://download.zope.org/distribution
    ...
    ... [packages]
    ... zip = False
    ... recipe = lovely.recipe:eggbox
    ... eggs = pytz
    ... excludes = ^pytz/zoneinfo/Mexico/.*
    ...
    ... [test]
    ... recipe = zc.recipe.egg:scripts
    ... eggs = lovely.recipe
    ... extra-paths = ${packages:path}
    ... interpreter = py
    ... """)
    >>> print system(buildout),
    Uninstalling packages.
    Installing packages.
    Installing test.
    Generated interpreter '/sample-buildout/bin/py'.

    >>> ls(sample_buildout + '/parts/packages')
    d  pytz
    >>> ls(sample_buildout + '/parts/packages/pytz/pytz/zoneinfo/Mexico')
    Traceback (most recent call last):
    ...
    OSError...No such file or directory: .../Mexico'

    >>> ls(sample_buildout + '/parts/packages/pytz/pytz/zoneinfo/America')
    -  Adak
    -  Anchorage
    -  Anguilla
    -  ...

Note that we still have the same directory structure as the zipped
version with a directory for each top-level namespace.


The test section uses the path of our packages section.

    >>> cat(sample_buildout + '/bin/py')
    #!...
    import sys
    <BLANKLINE>
    sys.path[0:0] = [.../sample-buildout/parts/packages/pytz',
      ]...

