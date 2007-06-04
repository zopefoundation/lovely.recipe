==========================
Filesystem Buildout Recipe
==========================

Creating Directories
====================

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... path = mystuff
    ... """)
    >>> print system(buildout),
    Installing data-dir.
    data-dir: Creating directory mystuff

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  mystuff
    d  parts

Creating Files
==============

The mkfile recipe creates a file with a given path, content and
permissions.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = script
    ...
    ... [script]
    ... recipe = lovely.recipe:mkfile
    ... path = file.sh
    ... content = hoschi
    ... mode = 0755
    ... """)
    >>> print system(buildout)
    Uninstalling data-dir.
    Installing script.
    script: Writing file /sample-buildout/file.sh
    <BLANKLINE>

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    -  file.sh
    d  parts

The content is written to the file.

    >>> cat(sample_buildout, 'file.sh')
    hoschi

And the mode is set.

    >>> import os, stat
    >>> path = os.path.join(sample_buildout, 'file.sh')
    >>> oct(stat.S_IMODE(os.stat(path)[stat.ST_MODE]))
    '0755'
