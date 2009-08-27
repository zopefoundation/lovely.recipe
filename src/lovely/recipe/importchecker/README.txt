====================
Importchecker Recipe
====================

This recipe creates an importchecker instance in the bin directory.


Creating The Script
===================

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = checker
    ...
    ... offline = true
    ...
    ... [checker]
    ... recipe = lovely.recipe:importchecker
    ... path = src/lovely
    ... """)
    >>> print system(buildout),
    Installing checker.
    checker: setting up importchecker
    Generated script 'bin/importchecker'.

    >>> import os
    >>> ls(os.path.join(sample_buildout, 'bin'))
    -  buildout
    -  importchecker

    >>> cat('bin', 'importchecker')
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
      ...
      ]
    <BLANKLINE>
    import lovely.recipe.importchecker.importchecker
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.importchecker.importchecker.main(['importchecker', 'src/lovely'])

