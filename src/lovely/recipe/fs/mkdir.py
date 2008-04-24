import os
import logging

class Mkdir:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.originalPath = options['path']
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              self.originalPath,
                              )
        self.createPath = options.get('createpath', 'False').lower() in ['true', 'on', '1']
        if (    not self.createPath
            and not os.path.isdir(os.path.dirname(options['path']))
           ):
            logging.getLogger(self.name).error(
                'Cannot create %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        if not os.path.isdir(path):
            logging.getLogger(self.name).info(
                'Creating directory %s', self.originalPath)
            os.makedirs(path)
        return ()

    def update(self):
        pass

