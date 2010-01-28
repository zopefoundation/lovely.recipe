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
    ... develop = %(loc)s
    ... parts = packages
    ... find-links = %(server)s
    ... index = %(server)s/index
    ...
    ... [packages]
    ... recipe = lovely.recipe:eggbox
    ... eggs = demo
    ...        lovely.recipe
    ... interpreter = py
    ... """ % dict(loc=lovely_recipy_loc, server=link_server))


    >>> print system(buildout)
    Develop: '...lovely.recipe'
    Getting distribution for 'demo'.
    Got demo 0.4c1.
    Getting distribution for 'demoneeded'.
    Got demoneeded 1.2c1.
    Installing packages.
    Generated script '...sample-buildout/bin/demo'.
    Generated interpreter '...sample-buildout/bin/py'.

We now have a zip file for each top-level directory. Note that the
zip-files are ending with .egg for pkg_resources compatibility.

    >>> ls(sample_buildout + '/parts/packages')
    -  easy_install.py.egg
    -  eggrecipedemo.py.egg
    -  eggrecipedemoneeded.py.egg
    -  lovely.egg
    -  pkg_resources.py.egg
    -  setuptools.egg
    -  zc.egg

The generated interpreter now has the demo zip file in the path.

    >>> cat(sample_buildout + '/bin/py')
    #!...
    sys.path[0:0] = [
      '/sample-buildout/parts/packages/easy_install.py.egg',
      '/sample-buildout/parts/packages/eggrecipedemo.py.egg',
      '/sample-buildout/parts/packages/eggrecipedemoneeded.py.egg',
      '/sample-buildout/parts/packages/lovely.egg',
      '/sample-buildout/parts/packages/pkg_resources.py.egg',
      '/sample-buildout/parts/packages/setuptools.egg',
      '/sample-buildout/parts/packages/zc.egg',
      ]...

It is possible to disable zipping. And also to exclude or include
patterns of files. So for example we can strip down the uneeded
setuptools egg. We can also create a script.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop = %(loc)s
    ... parts = packages test
    ... find-links = %(server)s
    ... index = %(server)s/index
    ...
    ... [packages]
    ... zip = False
    ... recipe = lovely.recipe:eggbox
    ... eggs = demo
    ...        lovely.recipe
    ... excludes = ^setuptools/.*
    ...            ^easy_install.*
    ...            ^pkg_resources.*
    ...
    ... [test]
    ... recipe = zc.recipe.egg:scripts
    ... eggs = lovely.recipe
    ... extra-paths = ${packages:path}
    ... interpreter = py
    ... """ % dict(loc=lovely_recipy_loc, server=link_server))
    >>> print system(buildout),
    Develop: '/Users/bd/sandbox/lovely.recipe'
    Uninstalling packages.
    Installing packages.
    Generated script '/sample-buildout/bin/demo'.
    Installing test.
    Generated interpreter '/sample-buildout/bin/py'.

Note that we still have the same directory structure as the zipped
version with a directory for each top-level namespace.  The 'lovely'
directory is not in he packages directory because it is a develop egg
and we have set zipped to false, therefore it is only added to the
python path.

    >>> ls(sample_buildout + '/parts/packages')
    d  eggrecipedemo.py
    d  eggrecipedemoneeded.py
    d  zc

    >>> print system(join(sample_buildout, 'bin', 'py') + \
    ...        ' -c "import lovely.recipe; print lovely.recipe.__file__"')
    /.../src/lovely/recipe/__init__.py...



The test section uses the path of our packages section. Note that due,
to the development path of lovely.recipe this path is actually
included twice because the script recipe does not check duplicates.

    >>> cat(sample_buildout + '/bin/py')
    #!...
    sys.path[0:0] = [
      '/...lovely.recipe/src',
      ...
      '/.../lovely.recipe/src',
      '/sample-buildout/parts/packages/eggrecipedemo.py',
      '/sample-buildout/parts/packages/eggrecipedemoneeded.py',
      '/sample-buildout/parts/packages/zc',
      ]...

