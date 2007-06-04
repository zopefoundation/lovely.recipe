import os
import logging

class Mkfile:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.mode = int(options.get('mode', '0644'), 8)
        options['content']
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              options['path'],
                              )
        if not os.path.isdir(os.path.dirname(options['path'])):
            logging.getLogger(self.name).error(
                'Cannot create file %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        f = file(path, 'w')
        logging.getLogger(self.name).info(
            'Writing file %s', path)
        f.write(self.options['content'])

        f.close()
        os.chmod(path, self.mode)
        return path

