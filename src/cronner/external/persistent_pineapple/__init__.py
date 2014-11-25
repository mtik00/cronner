#!/usr/bin/env python
'''
Persistent Pineapple provides a simple interface to save settings for
applications or other modules.  The settings file is in the JSON format for
simplicty.  A slightly modified JSON format is used to allow for comments and
other creature features.  Please read the _json.py file for more details.

Example settings file::
    .. literalinclude:: ../../../lib/tests/test1.json
        :linenos:

Example code:
    >>> settings = PersistentPineapple('/etc/myapp.json')
    >>> print settings.program_name
    myapp
    >>> if settings.debug:
    ...     print "we're in debug mode"
    we're in debug mode
    >>> settings.debug = False

'''

__author__ = "Timothy McFadden"
__copyright__ = "Copyright 2014"
__credits__ = ["Timothy McFadden", "Jason Unrein"]
__license__ = "GPL"
__version__ = "0.0.0.3"  # file version
__maintainer__ = "Jason Unrein"
__email__ = "JasonAUnrein@gmail.com"
__status__ = "Development"

# Imports #####################################################################
import os.path
from copy import copy
from ._json import JSON

# Globals #####################################################################
VERSION = "0.0.0.2"  # Library version


###############################################################################
class PersistentPineapple(object):
    '''An interface to the project settings.'''

    settings = {}

    def __init__(self, path, woc=True, lofc=True):
        '''
        Create a new instance or return the cached instance if the application
        has already created an instance with the specified path.  This is not
        a true singleton but a managed cache.

        path - Full directory/filename of where to load and save the file
        woc - Write On Change
        '''
        self.path = path
        self.woc = woc
        self.lofc = lofc

        self._settings_copy = None
        self._pre_context_woc = None

        if path and path not in self.settings:
            self.settings[path] = {}
            self._load()
            self.mtime = os.path.getmtime(self.path)
        elif path and path in self.settings:
            self.mtime = os.path.getmtime(self.path)
            return
        else:
            raise TypeError

    def _lofc(self):
        '''
        Load the new settings if the file has been modified since the last load
        '''
        if not self.lofc:
            return

        mtime = os.path.getmtime(self.path)
        if self.mtime < mtime:
            self.mtime = mtime
            self._load()

    def __getitem__(self, key):
        '''
        Return item defined by key from settings file.  If lofc was set, the
        contents of the settings file will be reloaded if the file has been
        modified since last read.
        '''
        self._lofc()
        return self.settings[self.path][key]

    def __setitem__(self, key, value):
        '''
        Set/overwrite the currently read item. If woc was set, the settings
        file will be overwritten with the new settings.
        '''
        self.settings[self.path][key] = value
        if self.woc:
            self.save()

    def __delitem__(self, key):
        '''Delete the item defined by key from the settings file'''
        del(self.settings[self.path][key])
        if self.woc:
            self.save()

    def __len__(self):
        '''Return the number of settings stored'''
        return len(self.settings[self.path])

    def __enter__(self):
        '''Make a copy of our settings for reapplication upon exit.
        We never want write-on-change to be True here, since this is assumed
        to be a temporary situation.
        '''
        self._pre_context_woc = self.woc
        self._settings_copy = copy(self.settings[self.path])
        self.woc = False

    def __exit__(self, exc_type, exc_value, traceback):
        '''Reapply the cached settings.'''
        self.settings[self.path] = copy(self._settings_copy)
        self.woc = self._pre_context_woc
        self._settings_copy = None
        self._pre_context_woc = None

    def __iter__(self):
        return (x for x in self.settings[self.path])

    def get(self, key):
        '''
        Return item defined by key from settings file.  If lofc was set, the
        contents of the settings file will be reloaded if the file has been
        modified since last read.
        '''
        self._lofc()
        return self.settings[self.path][key]

    def set(self, key, value):
        '''
        Set/overwrite the currently read item. If woc was set, the settings
        file will be overwritten with the new settings.
        '''
        self.settings[self.path][key] = value
        if self.woc:
            self.save()

    def _load(self):
        '''Do a fresh load of the settings file'''
        self.settings[self.path].clear()
        self.settings[self.path].update(JSON().load(path=self.path))

    def save(self, path=None):
        '''Save the settings back to the file'''
        if path is None:
            path = self.path

        JSON().store(self.settings[self.path], path)

    def reload(self):
        '''Reload the settings file'''
        self._load()
