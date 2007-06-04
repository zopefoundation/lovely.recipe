import os
import logging

class Mkdir:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              options['path'],
                              )
        if not os.path.isdir(os.path.dirname(options['path'])):
            logging.getLogger(self.name).error(
                'Cannot create %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        if not os.path.isdir(path):
            logging.getLogger(self.name).info(
                'Creating directory %s', os.path.basename(path))
            os.mkdir(path)
        return path


