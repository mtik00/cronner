'''
This module contains a wrapper for Python's built-in json module to make it
easier to use.
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
import json
import re
import sys


###############################################################################
def container_to_ascii(item):
    '''Converts all items from unicode to ascii, where needed.  This is a
    recursive function.  You may pass in any container or object, however,
    only basic types will be converted: scalars, lists, and dictionaries.
    Everything else will be ignored.

    Examples::
        >>> print(container_to_ascii(int(4)))
        4
        >>> print(container_to_ascii(['test', u'test']))
        ['test', 'test']
        >>> print(container_to_ascii({u'one': u'test', u'two': 2, u'three':
        ... {'test': 2}, 4: [1, 2, 3, u'four']}))
        {'one': 'test', 4: [1, 2, 3, 'four'], 'three': {'test': 2}, 'two': 2}
        >>>
    '''
    result = None

    if sys.version_info[0] == 2 and type(item) is unicode:
        result = item.encode('ascii')
    elif type(item) is list:
        result = map(lambda x: container_to_ascii(x), item[:])
    elif type(item) is dict:
        result = dict()
        for key, value in item.items():
            result[container_to_ascii(key)] = container_to_ascii(value)
    else:
        result = item

    return result


###############################################################################
class MyEncoder(json.JSONEncoder):
    '''Simple decoder that returns the dict of an object.'''
    def default(self, obj):
        return obj.__dict__


###############################################################################
class JSON(object):
    '''This object is used to load JSON data from a string or file.  It will
    remove any comment-only lines, and try to give some indication of why JSON
    failed to load (e.g. trailing comma).

    JSON reads much like Python; [] is for a list of items, {} is for a
    dictionary.

    Some important notes:

    * single-quotes (B{'}) are invalid; always use double-quotes (B{"})
    * A Python B{None} is represented by a JSON B{null}
    * A list cannot end with a trailing comma (a comma after the last item in the list)

    Comments:

    * JSON does not supports comments.  This functionality was added to this object to make life easier.

    We support the following types of comments

    * A line consisting of 0 or more whitespace characters followed by ``//``
    * Text ending a line with 1 or more whitespace characters followed
      by ``//``
    * All text in between ``/*`` and ``*/``

    Examples

        .. code-block:: python
            :linenos:

            // this line is ignored
            {"key": 5} // the rest of the line is ignored
            {"key": 5 /*,"key2": 6*/}  // key2 and the remainder is ignored
            {"key": 5}// INVALID!  You must have at least 1 whitespace character before // for hanging comments

    '''

    RE_TRAILING_COMMA = re.compile(r',\s*[,}\]]')
    RE_MISSING_VALUE = re.compile(r':\s*[,}\]]')
    RE_MISSING_COMMA = re.compile(r'[}\]]\s*[{\[]')

    def _prep_json_string(self, string):
        '''This functions prepares the string for JSON loading.  It will:
            -  check for trailing commas and raise a ValueError if found
            -  check for missing values and raise a ValueError if found
            -  remove all comments
            -  return an array of lines split on "\n" (so self.load errors make
                more sense)
        '''
        # Remove all comments
        string = re.sub(re.compile(r'((^\s*//|\s+//).*?$)|(/\*.*?\*/)',
                                   flags=re.MULTILINE | re.DOTALL),
                        '', string)

        # Check for trailing commas
        if self.RE_TRAILING_COMMA.search(string):
            location = string.find(
                self.RE_TRAILING_COMMA.search(string).group(0))
            context = string[location - 40:location + 10]
            raise ValueError("Trailing comma found in JSON string near: " +
                             context)

        # Check for missing values
        if self.RE_MISSING_VALUE.search(string):
            location = string.find(
                self.RE_MISSING_VALUE.search(string).group(0))
            context = string[location - 40:location + 10]
            raise ValueError("Missing value found in JSON string near: " +
                             context)

        # Check for missing commas
        if self.RE_MISSING_COMMA.search(string):
            location = string.find(
                self.RE_MISSING_COMMA.search(string).group(0))
            context = string[location - 40:location + 10]
            raise ValueError("Missing comma found in JSON string near: " +
                             context)

        lines = string.split("\n")
        lines = [x.strip() for x in lines if x.strip()]
        return lines

    def load(self, string=None, path=None, force_ascii=True):
        '''Loads JSON data from either a string or a file.'''
        if string is None and path is None:
            raise Exception("Must pass in either string or path")

        if string:
            lines = self._prep_json_string(string)
        elif path:
            with open(path, 'rb') as pfile:
                text = pfile.read().decode()
            lines = self._prep_json_string(text)
        else:
            raise ValueError("Must enter either string or path")

        try:
            json_data = json.loads('\n'.join(lines))
        except ValueError as err:
            if re.search(r"line (\d+)", err.message):
                line = int(re.search(r"line (\d+)", err.message).group(1))
                context = '\n'.join(lines[line - 4:line + 4])
                if ("Expecting property name" in err.message) and \
                   ("'" in context):
                    print("Possible invalid single-quote around here (JSON "
                          "only supports double-quotes):")
                    print(context)
                elif "Expecting property name" in err.message:
                    print("Possible trailing comma somewhere around here:")
                    print(context)
                else:
                    print("Error somewhere around here:")
                    print(context)
            raise

        if force_ascii:
            json_data = container_to_ascii(json_data)

        return json_data

    def store(self, data, path, cls=MyEncoder):
        '''Write the data to a JSON formatted file.'''
        if sys.version_info[0] == 3:
            bytedata = bytes(encode(data, cls), 'UTF-8')
        else:
            bytedata = encode(data, cls)
        with open(path, 'wb') as pfile:
            pfile.write(bytedata)


def encode(data, cls=MyEncoder):
    '''encode the provided data in JSON format'''
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '),
                      cls=cls)
