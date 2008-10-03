#!/usr/bin/env python
from setuptools import setup, find_packages
entry_points = """
[zc.buildout]
mkdir = lovely.recipe.fs.mkdir:Mkdir
mkfile = lovely.recipe.fs.mkfile:Mkfile
i18n = lovely.recipe.i18n.i18n:I18n
importchecker = lovely.recipe.importchecker.app:ImportChecker
instance = lovely.recipe.zope.zope:LovelyInstance
app = lovely.recipe.zope.zope:LovelyApp
server = lovely.recipe.zeo:LovelyServer
eggbox = lovely.recipe.egg:EggBox
"""

setup (
    name='lovely.recipe',
    description = "set of helper recipies for zc.buildout",
    version='1.0.0a1',
    author = "Lovely Systems",
    author_email = "office@lovelysystems.com",
    license = "ZPL 2.1",
    keywords = "buildout recipe filesystem i18n importchecker",
    url = 'http://launchpad.net/lovely.recipe',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['lovely', 'lovely.recipe'],
    extras_require = dict(zope=[
                        'zope.app.locales',
                        'zc.zope3recipes',
                        'zc.zodbrecipes',
                        'zope.app.locales>=3.4.5',
                        'ZConfig']),
    install_requires = ['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        ],
    entry_points = entry_points,
    zip_safe = True,
    )
