import logging
import os
import pwd
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
        owner = options.get('owner')
        if owner:
            try:
                uid = pwd.getpwnam(owner)[2]
            except KeyError:
                raise zc.buildout.UserError(
                    'The user %s does not exist.' % owner)
            if os.getuid() != 0:
                raise zc.buildout.UserError(
                    'Only root can change the owner to %s.' % owner)

            options['owner-uid'] = str(uid)

        self.createPath = options.get('createpath', 'False').lower() in [
            'true', 'on', '1']

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
        uid = self.options.get('owner-uid')
        if uid is not None:
            uid = int(uid)
            os.chown(path, uid, -1)
        return ()

    def update(self):
        pass

