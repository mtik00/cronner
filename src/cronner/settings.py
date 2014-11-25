#!/usr/bin/env python2.7
"""
This module holds the representation of the project settings.
"""

# Imports ######################################################################
from __future__ import print_function
from .external.persistent_pineapple import PersistentPineapple


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"

# Globals ######################################################################
SETTINGS = None


def _init(config_file):
    global SETTINGS
    SETTINGS = PersistentPineapple(config_file, woc=False, lofc=False)


def get_settings(config_file=None):
    if SETTINGS is None:
        _init(config_file)

    return SETTINGS
