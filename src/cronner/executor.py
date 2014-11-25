#!/usr/bin/env python2.7
"""
This script contains the wrapper code to run a command on the command-line.
"""

# Imports ######################################################################
from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/23/2014"
__license__ = "MIT"
__version__ = "0.01"

# Globals ######################################################################
DEBUG = False


def execute(command, shell=None, working_dir="."):
    """Execute a command on the command-line.

    :param command str/list: The command to run
    :param shell bool: Whether or not to use the shell.  This is optional; if
        `command` is a basestring, shell will be set to True, otherwise it will
        be false.  You can override this behavior by setting this parameter
        directly.
    :param working_dir str: The directory in which to run the command.

    :returns: tuple: (return code, stdout)
    """
    if shell is None:
        shell = True if isinstance(command, basestring) else False

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=shell, cwd=working_dir)

    stdout, _ = p.communicate()

    return (p.returncode, stdout)
