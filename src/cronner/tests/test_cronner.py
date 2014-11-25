#!/usr/bin/env python
"""
This is the unit test for "cronner".
"""
# Imports ######################################################################
from __future__ import print_function
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cronner


class Test(unittest.TestCase):

    def test_version(self):
        print(cronner.__version__)


if __name__ == '__main__':
    unittest.main()
