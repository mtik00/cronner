#!/usr/bin/env python
__author__ = "Timothy McFadden"
__date__ = "11/25/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "0.01"
"""
This is the unit test for "cronner".
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cronner


class Test(unittest.TestCase):

    def test_f1(self):
        cronner.f1("testing")


if __name__ == '__main__':
    unittest.main()
