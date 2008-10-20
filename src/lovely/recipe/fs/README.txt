==========================
Filesystem Buildout Recipe
==========================

Creating Directories
====================

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
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

If we change the directory name the old directory ('mystuff') is not deleted.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... path = otherdir
    ... """)
    >>> print system(buildout),
    Uninstalling data-dir.
    Installing data-dir.
    data-dir: Creating directory otherdir

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  mystuff
    d  otherdir
    d  parts

We can also create a full path.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... path = with/subdir
    ... """)
    >>> print system(buildout),
    Uninstalling data-dir.
    Installing data-dir.
    data-dir: Cannot create /sample-buildout/with/subdir. /sample-buildout/with is not a directory.
    While:
      Installing data-dir.
    Error: Invalid Path

But we need to activate this function explicitely.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... createpath = True
    ... path = with/subdir
    ... """)
    >>> print system(buildout),
    Installing data-dir.
    data-dir: Creating parent directory /sample-buildout/with
    data-dir: Creating directory with/subdir

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  mystuff
    d  otherdir
    d  parts
    d  with
    >>> ls(sample_buildout + '/with')
    d  subdir


We can change the owner of the created directory if run as root. This is tested
in mkdir-root.txt.

If not run as root, setting the owner is an error:

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... createpath = True
    ... path = another/with/subdir
    ... owner = nobody
    ... """)
    >>> print system(buildout),
    While:
      Installing.
      Getting section data-dir.
      Initializing part data-dir.
    Error: Only root can change the owner to nobody.


It is an error when the user does not exist:

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = data-dir
    ... find-links = http://download.zope.org/distribution
    ...
    ... [data-dir]
    ... recipe = lovely.recipe:mkdir
    ... createpath = True
    ... path = another/with/subdir
    ... owner = someuser
    ... """)
    >>> print system(buildout),
    While:
      Installing.
      Getting section data-dir.
      Initializing part data-dir.
    Error: The user someuser does not exist.


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
    d  mystuff
    d  otherdir
    d  parts
    d  with

The content is written to the file.

    >>> cat(sample_buildout, 'file.sh')
    hoschi

And the mode is set.

    >>> import os, stat
    >>> path = os.path.join(sample_buildout, 'file.sh')
    >>> oct(stat.S_IMODE(os.stat(path)[stat.ST_MODE]))
    '0755'

If we change the filename the old file is deleted.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = script
    ...
    ... [script]
    ... recipe = lovely.recipe:mkfile
    ... path = newfile.sh
    ... content = hoschi
    ... mode = 0755
    ... """)
    >>> print system(buildout)
    Uninstalling script.
    Installing script.
    script: Writing file /sample-buildout/newfile.sh
    <BLANKLINE>

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  mystuff
    -  newfile.sh
    d  otherdir
    d  parts
    d  with

We can also specify to create the path for the file.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = script
    ...
    ... [script]
    ... recipe = lovely.recipe:mkfile
    ... createpath = On
    ... path = subdir/for/file/file.sh
    ... content = hoschi
    ... mode = 0755
    ... """)
    >>> print system(buildout)
    Uninstalling script.
    Installing script.
    script: Creating directory /sample-buildout/subdir/for/file
    script: Writing file /sample-buildout/subdir/for/file/file.sh

    >>> ls(sample_buildout + '/subdir/for/file')
    -  file.sh

