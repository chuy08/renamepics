#
# Standard libraries
#
from os import path
from setuptools import setup, find_packages

#
# Third party libraries
#

#
# Internal libraries
#
from rename.__init__ import __version__

try:
    with open(path.join(path.dirname(__file__), 'README.md')) as f:
        long_description = f.read()
except Exception:
    # XXX: Intentional pokemon catch to prevent this read from breaking setup.py
    long_description = None

# Pull the name and version from our application object
NAME = 'renamePics'

VERSION = __version__

# URL to the repository on Github.
REPO_URL = 'https://github.com/chuy08/renamepics'
# Github will generate a tarball as long as you tag your releases, so don't forget to tag!
# We use the application version to construct the DOWNLOAD_URL.
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))

setup(
    name=NAME,
    version=VERSION,
    author='Jesus Orosco',
    author_email='chuy08@gmail.com',
    description='Sort pictures and video based on Exif data',
    long_description=long_description,
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    license='All Rights Reserved.',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': [
            '{name} = rename.cli:main'.format(name=NAME),
        ]
    },
    python_requires='~=3.6',
)
