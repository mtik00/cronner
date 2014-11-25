#!/usr/bin/env python
"""This module is used to provide functionality to
`python -m cronner`

By default, it will print out the module name, version, and location.
"""
from __future__ import print_function
from os import path
import sys


if __name__ == '__main__':
    # Read the version from our project
    this_directory = path.abspath(path.dirname(__file__))
    package_dir = path.join(this_directory, "..")
    sys.path.insert(0, package_dir)
    from cronner import __version__

    print("running [{0}] version [{1}] from [{2}]".format(
        "cronner", __version__, this_directory))
