import os
import logging
import zc.buildout


class Mkdir(object):

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

    def install(self):
        path = self.options['path']
        dirname = os.path.dirname(self.options['path'])

        if not os.path.isdir(dirname):
            if self.createPath:
                logging.getLogger(self.name).info(
                    'Creating parent directory %s', dirname)
                os.makedirs(dirname)
            else:
                logging.getLogger(self.name).error(
                    'Cannot create %s. %s is not a directory.',
                    path, dirname)
                raise zc.buildout.UserError('Invalid Path')

        if not os.path.isdir(path):
            logging.getLogger(self.name).info(
                'Creating directory %s', self.originalPath)
            os.mkdir(path)
        return ()

    def update(self):
        pass

