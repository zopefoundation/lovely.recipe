import os
import logging


class Mkfile(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.mode = int(options.get('mode', '0644'), 8)
        options['content']
        self.originalPath = options['path']
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              self.originalPath,
                              )
        self.createPath = options.get('createpath', 'False').lower() in ['true', 'on', '1']

    def install(self):
        filename = self.options['path']
        dirname = os.path.dirname(self.options['path'])

        if not os.path.isdir(dirname):
            if self.createPath:
                logging.getLogger(self.name).info(
                    'Creating directory %s', dirname)
                os.makedirs(dirname)
            else:
                logging.getLogger(self.name).error(
                    'Cannot create file %s. %s is not a directory.',
                    filename, dirname)
                raise zc.buildout.UserError('Invalid path')

        f = file(filename, 'w')
        logging.getLogger(self.name).info(
            'Writing file %s', filename)
        f.write(self.options['content'])
        f.close()
        os.chmod(filename, self.mode)
        return filename
