#!/usr/bin/env python
__author__ = "FULLNAME"
__date__ = "99/99/9999"
__copyright__ = "FULLNAME, CURRENTYEAR"
__license__ = "MIT"
__version__ = "0.01"
"""
This is the unit test for SAMPEPROJ.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import SAMPLEPROJ


class Test(unittest.TestCase):

    def test_f1(self):
        SAMPLEPROJ.f1("testing")


if __name__ == '__main__':
    unittest.main()
