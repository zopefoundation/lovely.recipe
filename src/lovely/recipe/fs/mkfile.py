import os
import logging

class Mkfile:

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
        if (    not self.createPath
            and not os.path.isdir(os.path.dirname(options['path']))
           ):
            logging.getLogger(self.name).error(
                'Cannot create file %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        if self.createPath:
            logging.getLogger(self.name).info(
                'Creating directory %s', os.path.dirname(self.options['path']))
            os.makedirs(os.path.dirname(self.options['path']))
        f = file(path, 'w')
        logging.getLogger(self.name).info(
            'Writing file %s', path)
        f.write(self.options['content'])

        f.close()
        os.chmod(path, self.mode)
        return path

