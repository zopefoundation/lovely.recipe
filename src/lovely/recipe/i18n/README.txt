=================
i18n Tools Recipe
=================

This recipe allows to create i18n tools to extract and merge po files.


Creating The Tools
==================

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = i18n
    ...
    ... find-links = http://download.zope.org/distribution
    ... offline = true
    ...
    ... [i18n]
    ... recipe = lovely.recipe:i18n
    ... package = lovely.recipe
    ... domain = recipe
    ... location = src/somewhere
    ... output = locales
    ... zcml = src/somewhere/configure.zcml
    ... maker = z3c.csvvocabulary.csvStrings
    ... """)
    >>> print system(buildout),
    Installing i18n.
    i18n: setting up i18n tools
    Generated script 'bin/i18nextract'.
    Generated script 'bin/i18nmergeall'.

    >>> import os
    >>> ls(os.path.join(sample_buildout, 'bin'))
    -  buildout
    -  i18nextract
    -  i18nmergeall

    >>> cat('bin', 'i18nextract')
    #!/opt/local/bin/python
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
      ,
      ]
    <BLANKLINE>
    import lovely.recipe.i18n.i18nextract
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.i18n.i18nextract.main()

