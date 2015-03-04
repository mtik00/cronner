#!/usr/bin/env python
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


# Globals ######################################################################
DEBUG = False


def execute(command, shell=None, working_dir=".", echo=False, echo_indent=0):
    """Execute a command on the command-line.

    :param str,list command: The command to run
    :param bool shell: Whether or not to use the shell.  This is optional; if
        ``command`` is a basestring, shell will be set to True, otherwise it will
        be false.  You can override this behavior by setting this parameter
        directly.
    :param str working_dir: The directory in which to run the command.
    :param bool echo: Whether or not to print the output from the command to
        stdout.
    :param int echo_indent: Any number of spaces to indent the echo for clarity

    :returns: tuple: (return code, stdout)

    Example

        >>> from executor import execute
        >>> return_code, text = execute("dir")
    """
    if shell is None:
        shell = True if isinstance(command, basestring) else False

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=shell, cwd=working_dir)

    if echo:
        stdout = ""
        while p.poll() is None:
            line = p.stdout.readline()  # This blocks until it receives a newline.
            print(" " * echo_indent, line, end="")
            stdout += line

        # Read any last bits
        line = p.stdout.read()
        print(" " * echo_indent, line, end="")
        print()
        stdout += line
    else:
        stdout, _ = p.communicate()

    return (p.returncode, stdout)
