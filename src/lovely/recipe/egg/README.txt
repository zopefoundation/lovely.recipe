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

    >>> import os
    >>> lovely_recipy_loc = os.path.dirname(os.path.dirname(os.path.dirname(
    ...     os.path.dirname(os.path.dirname(__file__)))))

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop = %s
    ... parts = packages
    ...
    ... [packages]
    ... recipe = lovely.recipe:eggbox
    ... eggs = pytz
    ...        lovely.recipe
    ... interpreter = py
    ... """ % lovely_recipy_loc)

    >>> 'Installing packages.' in system(buildout + ' -o')
    True


We now have a zip file for each top-level directory. Note that the
zip-files are ending with .egg for pkg_resources compatibility.

    >>> ls(sample_buildout + '/parts/packages')
    -  lovely.egg
    -  pytz.egg
    -  zc.egg

The generated interpreter now has the pytz zip file in the path.

    >>> cat(sample_buildout + '/bin/py')
    #!...
    sys.path[0:0] = [
      '/sample-buildout/parts/packages/lovely.egg',
      '/sample-buildout/parts/packages/pytz.egg',
      '/sample-buildout/parts/packages/zc.egg',
      ]...

It is possible to disable zipping. And also to exclude or include
patterns of files. So for example we can strip down pytz. We can also
create a script.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop = %s
    ... parts = packages test
    ... find-links = http://download.zope.org/distribution
    ...
    ... [packages]
    ... zip = False
    ... recipe = lovely.recipe:eggbox
    ... eggs = pytz
    ...        lovely.recipe
    ... excludes = ^pytz/zoneinfo/Mexico/.*
    ...
    ... [test]
    ... recipe = zc.recipe.egg:scripts
    ... eggs = lovely.recipe
    ... extra-paths = ${packages:path}
    ... interpreter = py
    ... """ % lovely_recipy_loc)
    >>> print system(buildout),
    Develop: '...'
    Uninstalling packages.
    Installing packages.
    Installing test.
    Generated interpreter '/sample-buildout/bin/py'.

Note that we still have the same directory structure as the zipped
version with a directory for each top-level namespace.  The 'lovely'
directory is not in he packages directory because it is a develop egg
and we have set zipped to false, therefore it is only added to the
python path.

    >>> ls(sample_buildout + '/parts/packages')
    d  pytz
    d  zc

    >>> print system(join(sample_buildout, 'bin', 'py') + \
    ...        ' -c "import lovely.recipe; print lovely.recipe.__file__"')
    /.../src/lovely/recipe/__init__.py...



    >>> ls(sample_buildout + '/parts/packages/pytz/pytz/zoneinfo/Mexico')
    Traceback (most recent call last):
    ...
    OSError...No such file or directory: .../Mexico'

    >>> ls(sample_buildout + '/parts/packages/pytz/pytz/zoneinfo/America')
    -  Adak
    -  Anchorage
    -  Anguilla
    -  ...

The test section uses the path of our packages section. Note that due,
to the development path of lovely.recipe this path is actually
included twice because the script recipe does not check duplicates.

    >>> cat(sample_buildout + '/bin/py')
    #!...
    sys.path[0:0] = [
      '/.../src',
      '/Users/bd/.buildout/eggs/zc.recipe.egg-...egg',
      '/sample-buildout/eggs/zc.buildout-...egg',
      '/opt/local/lib/python2.5/site-packages',
      '/.../src',
      '/sample-buildout/parts/packages/pytz',
      '/sample-buildout/parts/packages/zc',
      ]...


