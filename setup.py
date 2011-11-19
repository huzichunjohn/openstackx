import os
import shutil
import sys
import time

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

TOPDIR = os.path.abspath(os.path.dirname(__file__))
VFILE  = os.path.join(TOPDIR, 'openstackx', '__pistonversion__.py')

args = filter(lambda x: x[0] != '-', sys.argv)
command = args[1] if len(args) > 1 else ''

if command == 'sdist':
    PISTON_VERSION = os.environ['PISTON_VERSION']
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command == 'develop':
    PISTON_VERSION = time.strftime('9999.0.%Y%m%d%H%M%S', time.localtime())
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command is None:
    PISTON_VERSION = '9999999999-You_did_not_set_a_version'
else:
    assert os.path.exists(VFILE), 'version.py does not exist, please set PISTON_VERSION (or run make_version.py for dev purposes)'
    from openstackx import __pistonversion__ as pistonversion
    PISTON_VERSION = pistonversion.VERSION

dst = 'debian/openstackx/var/lib/nova/'
os.system('rm -rf %s' % dst)
shutil.copytree('extensions', '%s/extensions' % dst)

requirements = ['httplib2']
if sys.version_info < (2,6):
    requirements.append('simplejson')

setup(
    name = "openstackx",
    version = PISTON_VERSION,
    description = "Client library extensions for the OpenStack API",
    long_description = read('README.rst'),
    url = 'http://github.com/cloudbuilders/openstackx/',
    license = 'Apache 2.0',
    author = 'Anthony Young',
    author_email = 'sleepsonthefloor@gmail.com',
    packages = find_packages(exclude=['tests']),
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    namespace_packages = ["openstackx"],
    install_requires = requirements,
    tests_require = ["nose", "mock"],
    test_suite = "nose.collector",
)

