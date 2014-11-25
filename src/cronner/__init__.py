#!/usr/bin/env python
"""
This module does awesome stuff!

Example::

    >>> from __future__ import print_function
    >>> from cronner import f1
    >>> f1(1)
    >>>
"""
# Imports ######################################################################
from __future__ import print_function
from cronner.logger import get_logger

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__createDate__ = "11/25/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"
VERSION = __version__  # For compatibility with other models


# Globals ######################################################################
def f1(something):
    """This function prints out the input and logs a message to the logger.

    :param variable something: The thing you want to print
    :returns: None
    """
    print("Hello World!", something)
    get_logger().critical("Hello again")
