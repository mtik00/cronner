#!/usr/bin/env python
'''SAMPLEPROJ package setup script.'''
from __future__ import print_function
import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(THIS_DIR, 'SAMPLEPROJ', '__init__.py')

# Read the version from our project
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_DIR = os.path.join(THIS_DIR, 'src')
sys.path.insert(0, PKG_DIR)
from SAMPLEPROJ import __version__


if __name__ == '__main__':
    setup(
        name="SAMPLEPROJ",
        version=__version__,
        description="Data SAMPLEPROJ package",
        author="<full name>",
        url="https://github.com/<username>/SAMPLEPROJ",
        install_requires=[],
        packages=find_packages(),
        package_data={"SAMPLEPROJ": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="tests",

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Other Environment',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: OS Independent',
        ],

        long_description=open(os.path.join(THIS_DIR, "README.rst"), 'r').read()
    )
