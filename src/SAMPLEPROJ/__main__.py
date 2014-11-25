#!/usr/bin/env python
from __future__ import print_function
from os import path
import sys


# Read the version from our project
this_directory = path.abspath(path.dirname(__file__))
package_dir = path.join(this_directory, "..")
sys.path.insert(0, package_dir)
from SAMPLEPROJ import __version__


print("running [{0}] version [{1}] from [{2}]".format(
    "SAMPLEPROJ", __version__, this_directory))
