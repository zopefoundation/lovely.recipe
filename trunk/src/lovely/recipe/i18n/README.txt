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
    ... index = http://download.zope.org/zope3.4
    ... offline = true
    ...
    ... [i18n]
    ... recipe = lovely.recipe:i18n
    ... package = lovely.recipe
    ... domain = recipe
    ... location = src/somewhere
    ... output = locales
    ... maker = z3c.csvvocabulary.csvStrings
    ... """)
    >>> print system(buildout),
    Installing i18n.
    i18n: setting up i18n tools
    Generated script 'bin/i18nextract'.
    Generated script 'bin/i18nmergeall'.
    Generated script 'bin/i18nstats'.

    >>> import os
    >>> ls(os.path.join(sample_buildout, 'bin'))
    -  buildout
    -  i18nextract
    -  i18nmergeall
    -  i18nstats


The i18n Extractor
------------------

    >>> cat('bin', 'i18nextract')
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
    ...
      ]
    <BLANKLINE>
    import lovely.recipe.i18n.i18nextract
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.i18n.i18nextract.main(['i18nextract', '-d', 'recipe', '-s', '/sample-buildout/parts/i18n/configure.zcml', '-p', 'src/somewhere', '-o', 'locales', '-m', 'z3c.csvvocabulary.csvStrings'])

We have a configure.zcml created.

    >>> cat('parts', 'i18n', 'configure.zcml')
    <configure xmlns='http://namespaces.zope.org/zope'>
      <include package="lovely.recipe" />
    </configure>


i18n Merge
----------

    >>> cat('bin', 'i18nmergeall')
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
    ...
      ]
    <BLANKLINE>
    import lovely.recipe.i18n.i18nmergeall
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.i18n.i18nmergeall.main(['i18nmergeall', '-l', 'src/somewhere/locales'])

i18n Stats
----------

    >>> cat('bin', 'i18nstats')
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
    ...
      ]
    <BLANKLINE>
    import lovely.recipe.i18n.i18nstats
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.i18n.i18nstats.main(['i18nstats', '-l', 'src/somewhere/locales'])


Tool Names
----------

The created tools are named after the section name. If the section for the
recipe is named 'translation' then the tools are named 'translationextract'
and 'translationmergeall'.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... index = http://download.zope.org/zope3.4
    ... parts = translation
    ...
    ... offline = true
    ...
    ... [translation]
    ... recipe = lovely.recipe:i18n
    ... package = lovely.recipe
    ... domain = recipe
    ... location = src/somewhere
    ... output = locales
    ... maker = z3c.csvvocabulary.csvStrings
    ... """)
    >>> print system(buildout),
    Uninstalling i18n.
    Installing translation.
    translation: setting up i18n tools
    Generated script 'bin/translationextract'.
    Generated script 'bin/translationmergeall'.
    Generated script 'bin/translationstats'.


Adding a custom configure.zcml
------------------------------

The created configure.zcml includes the package an assumes that the package
contains a configure.zcml. If this is not the case or if additional package
includes are needed then the zcml parameter can be used to define the content
of the generated configure.zcml.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = i18n
    ...
    ... offline = true
    ...
    ... [i18n]
    ... recipe = lovely.recipe:i18n
    ... package = lovely.recipe
    ... domain = recipe
    ... location = src/somewhere
    ... output = locales
    ... maker = z3c.csvvocabulary.csvStrings
    ... zcml =
    ...    <include package='zope.component' file='meta.zcml' />
    ...    <include package='lovely.recipe' />
    ...
    ... """)

    >>> print system(buildout),
    Uninstalling translation.
    Installing i18n.
    i18n: setting up i18n tools
    Generated script 'bin/i18nextract'.
    Generated script 'bin/i18nmergeall'.
    Generated script 'bin/i18nstats'.

    >>> cat('bin', 'i18nextract')
    #!...
    <BLANKLINE>
    import sys
    sys.path[0:0] = [
    ...
      ]
    <BLANKLINE>
    import lovely.recipe.i18n.i18nextract
    <BLANKLINE>
    if __name__ == '__main__':
        lovely.recipe.i18n.i18nextract.main(['i18nextract', '-d', 'recipe', '-s', '/sample-buildout/parts/i18n/configure.zcml', '-p', 'src/somewhere', '-o', 'locales', '-m', 'z3c.csvvocabulary.csvStrings'])

And the generated configure-zcml contains our extra code.

    >>> cat('parts', 'i18n', 'configure.zcml')
    <configure xmlns='http://namespaces.zope.org/zope'
               xmlns:meta="http://namespaces.zope.org/meta"
               >
    <BLANKLINE>
    <BLANKLINE>
    <include package='zope.component' file='meta.zcml' />
    <include package='lovely.recipe' />
    <BLANKLINE>
    </configure>

