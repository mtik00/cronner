#!/usr/bin/env python
"""
This module creates and initializes a project-wide logger.

Example::

    >>> from cronner.logger import get_logger()
    >>> get_logger.debug("test")
    >>>
"""
# Imports ######################################################################
from __future__ import print_function
import os
import logging


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__creationDate__ = "11/25/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
LOGGER = None

LOGFILE_DIR = "."
LOGFILE_NAME = "cronner-log.txt"
LOGFILE_FORMATTER = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
LOGFILE_LEVEL = logging.DEBUG

SCREEN_FORMATTER = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
SCREEN_LEVEL = logging.INFO


def _init():
    global LOGGER

    if LOGGER is None:
        LOGGER = logging.getLogger('cronner')
        LOGGER.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setFormatter(SCREEN_FORMATTER)
        ch.setLevel(SCREEN_LEVEL)
        LOGGER.addHandler(ch)

        if LOGFILE_NAME:
            path = os.path.join(LOGFILE_DIR, LOGFILE_NAME)
            fh = logging.FileHandler(path)
            fh.setLevel(LOGFILE_LEVEL)
            fh.setFormatter(SCREEN_FORMATTER)
            LOGGER.addHandler(fh)


def get_logger():
    if LOGGER is None:
        _init()

    return LOGGER
