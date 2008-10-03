import logging, os
import zc.recipe.egg
import shutil
import re
import pkg_resources
from zc.buildout.easy_install import _script

log = logging.getLogger(__name__)

SKIPPED_LIBDIRS = ('site-packages',)

class EggBox(zc.recipe.egg.Scripts):

    src_exclude = re.compile(r'.*/site-packages')
    includes = []
    excludes = [re.compile(r'(EGG-INFO)|(.*\.egg-info)|(.*\.pyc)|(.*\.svn/.*)'),
                re.compile(r'(^[^/]+\.txt)|(^setup\.[^/]+)|(^.[A-Z]+(\.[^/]+)?$)'),
                ]

    def __init__(self, buildout, name, options):
        options['parts-directory'] = buildout['buildout']['parts-directory']
        super(EggBox, self).__init__(buildout, name, options)
        # we need to do this on init because the signature cannot be
        # created if the egg is not already there
        self.ws = self.working_set()[1]
        self.zip = self.options.get('zip') != 'False'
        self.location = self.options.get(
            'location',
            os.path.join(self.options['parts-directory'], self.name))
        if options.get('includes'):
            self.includes += map(re.compile, options.get('includes').strip().split())
        if options.get('excludes'):
            self.excludes += map(re.compile, options.get('excludes').strip().split())
        self._mk_zips()

    def progress_filter(self, packages):
        def _pf(src, dst, packages=packages, includes=self.includes,
                excludes=self.excludes):
            for pat in includes:
                import pdb;pdb.set_trace()
                if not pat.match(src):
                    return None
            for pat in excludes:
                if pat.match(src):
                    return None
            return dst
        return _pf

    def genScript(self, paths):
        pass

    def install(self):
        scripts = self.options.get('scripts')
        reqs, ws = self.working_set()
        if scripts or scripts is None:
            if scripts is not None:
                scripts = scripts.split()
                scripts = dict([
                    ('=' in s) and s.split('=', 1) or (s, s)
                    for s in scripts
                    ])

            for s in self.options.get('entry-points', '').split():
                parsed = self.parse_entry_point(s)
                if not parsed:
                    log.error(
                        "Cannot parse the entry point %s.", s)
                    raise zc.buildout.UserError("Invalid entry point")
                reqs.append(parsed.groups())
            return self._mk_scripts(
                reqs, ws, self.options['executable'],
                self.options['bin-directory'],
                scripts=scripts,
                extra_paths=self.extra_paths,
                interpreter=self.options.get('interpreter'),
                initialization=self.options.get('initialization', ''),
                arguments=self.options.get('arguments', ''),
                )
        return ()
    update = install

    def _mk_zips(self):
        from setuptools import archive_util
        from setuptools.command.bdist_egg import  make_zipfile
        if os.path.isdir(self.location):
            shutil.rmtree(self.location)
        os.mkdir(self.location)
        dsts = []
        for src, names in self.ws.entry_keys.items():
            if self.src_exclude.match(src):
                continue
            log.debug("Adding archive %r %r" % (src, names))
            archive_util.unpack_archive(
                src, self.location, progress_filter=self.progress_filter(names))

        # let us put the things in seperate paths so we dont have to
        # care if we are zipped or not, we just have to add any
        # subitem in the packcage directory to the paht, not the
        # package directory itself
        tmp = os.path.join(self.location, '.tmp')
        for name in os.listdir(self.location):
            if name == '.tmp':
                continue
            os.mkdir(tmp)
            d = os.path.join(self.location, name)
            td = os.path.join(tmp, name)
            os.rename(d, td)
            os.rename(tmp, d)

        if self.zip:
            for name in os.listdir(self.location):
                d = os.path.join(self.location, name)
                # hm we need to call this .egg because of
                # pkg_resources.resource_filename
                z = os.path.join(self.location, name + '.egg')
                make_zipfile(z, d)
                shutil.rmtree(d)
        path = []
        for name in os.listdir(self.location):
            path.append(os.path.join(self.location, name))
        self.options['path'] = '\n'.join(path)
        self.path = path

    def _mk_scripts(self, reqs, working_set, executable, dest,
                scripts=None,
                extra_paths=(),
                arguments='',
                interpreter=None,
                initialization='',
                ):
        path = list(self.path)
        path.extend(extra_paths)
        path = repr(path)[1:-1].replace(', ', ',\n  ')
        generated = []

        if isinstance(reqs, str):
            raise TypeError('Expected iterable of requirements or entry points,'
                            ' got string.')

        if initialization:
            initialization = '\n'+initialization+'\n'

        entry_points = []
        for req in reqs:
            if isinstance(req, str):
                req = pkg_resources.Requirement.parse(req)
                dist = working_set.find(req)
                for name in pkg_resources.get_entry_map(dist, 'console_scripts'):
                    entry_point = dist.get_entry_info('console_scripts', name)
                    entry_points.append(
                        (name, entry_point.module_name,
                         '.'.join(entry_point.attrs))
                        )
            else:
                entry_points.append(req)

        for name, module_name, attrs in entry_points:
            if scripts is not None:
                sname = scripts.get(name)
                if sname is None:
                    continue
            else:
                sname = name

            sname = os.path.join(dest, sname)
            generated.extend(
                _script(module_name, attrs, path, sname, executable, arguments,
                        initialization)
                )

        if interpreter:
            sname = os.path.join(dest, interpreter)
            generated.extend(_pyscript(path, sname, executable))

        return generated
