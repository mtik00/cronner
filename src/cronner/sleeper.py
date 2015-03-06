#!/usr/bin/env python
"""
This module implements the "computer sleep" interface for the application.
"""
# Imports ######################################################################
from __future__ import print_function
import sys

if 'win' in sys.platform:
    import ctypes
    import win32api
    import win32security
else:
    print("WARNING: cronner.sleeper not implemented on non-Windows OS")


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "02/28/2015"
__license__ = "MIT"
__version__ = "0.01"


# Globals ######################################################################
def _windows_sleep():
    '''Put a Windows computer to sleep.'''
    # This function was taken from:  http://permalink.gmane.org/gmane.comp.python.windows/7382

    #
    # Enable the SeShutdown privilege (which must be present in your
    # token in the first place)
    #
    priv_flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    htoken = win32security.OpenProcessToken(
        win32api.GetCurrentProcess(),
        priv_flags
    )
    priv_id = win32security.LookupPrivilegeValue(
        None,
        win32security.SE_SHUTDOWN_NAME
    )
    win32security.AdjustTokenPrivileges(
        htoken,
        0,
        [(priv_id, win32security.SE_PRIVILEGE_ENABLED)]
    )

    #
    # Params:
    # True=> Standby; False=> Hibernate
    # True=> Force closedown; False=> Don't force
    #
    ctypes.windll.kernel32.SetSystemPowerState(True, True)


def sleep_pc():
    '''Calling this function will put your computer to sleep, if implemented.'''
    if 'win' in sys.platform:
        _windows_sleep()
    else:
        raise NotImplementedError()
