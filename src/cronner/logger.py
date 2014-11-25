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
import logging
from .settings import get_settings


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
LOGGER = None
SCREEN_LEVEL = logging.INFO


def _init(logfile=None):
    """Initializes the logging object.

    :param str logfile: The path of the log file, if any
    """
    global LOGGER
    settings = get_settings()

    if LOGGER is None:
        LOGGER = logging.getLogger("cronner")
        LOGGER.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        screen_formatter = logging.Formatter(settings["screen-formatter"])
        ch.setFormatter(screen_formatter)
        ch.setLevel(SCREEN_LEVEL)
        LOGGER.addHandler(ch)

        if logfile:
            logfile_formatter = logging.Formatter(settings["log-file-formatter"])
            fh = logging.FileHandler(logfile, settings["log-file-mode"])
            fh.setLevel(settings["log-file-level"])
            fh.setFormatter(logfile_formatter)
            LOGGER.addHandler(fh)


def get_logger(logfile=None):
    """Retrieves the global logging object."""
    if LOGGER is None:
        _init(logfile)

    return LOGGER
