from zc.buildout import testing

def setUpBuildout(test):
    testing.buildoutSetUp(test)
    testing.install_develop('zc.recipe.egg', test)
    testing.install_develop('lovely.recipe', test)
    testing.install_develop('zope.testing', test)
    testing.install_develop('zope.interface', test)
