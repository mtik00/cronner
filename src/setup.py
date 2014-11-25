#!/usr/bin/env python
'''cronner package setup script.'''
from __future__ import print_function
import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)

# Read the version from our project
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_DIR = os.path.join(THIS_DIR, 'src')
sys.path.insert(0, PKG_DIR)
from cronner import __version__


if __name__ == '__main__':
    setup(
        name="cronner",
        version=__version__,
        description="cronner package",
        author="Timothy McFadden",
        url="https://github.com/mtik00/cronner",
        install_requires=[],
        packages=find_packages(),
        package_data={"cronner": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="cronner.tests",

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
