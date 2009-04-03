import os
import logging
import zc.buildout

class Mkfile(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.mode = int(options.get('mode', '0644'), 8)
        self.variations = options.get('variations', '').strip().split()
        options['content']
        self.originalPath = options['path']
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              self.originalPath,
                              )
        self.createPath = options.get('createpath', 'False').lower() \
            in ['true', 'on', '1']

    def _write(self, variation):
        d = dict(variation=variation)
        filename = self.options['path'] % d
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
        f.write(self.options['content'] % d)
        f.close()
        os.chmod(filename, self.mode)
        return filename

    def install(self):
        res = []
        if self.variations:
            for v in self.variations:
                res.append(self._write(v))
        else:
            res.append(self._write(None))
        return res
