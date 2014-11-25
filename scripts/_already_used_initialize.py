#!/usr/bin/env python
"""
This script is used initialize the sample project with user-specific values
"""

# Imports ######################################################################
from __future__ import print_function
import os
import re
import sys
import time
import shutil

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__creationDate__ = "11/25/2014"
__license__ = "MIT"
__version__ = "0.01"


# Globals ######################################################################
DEBUG = False


def get_user_data():
    project_name = user_input("Enter the name of your new project: ")
    fullname = user_input("Enter your full name (e.g. Firstname Lastname): ")
    github_username = user_input("Enter your github username: ")
    github_project = user_input("Enter the name of your github project", default=project_name.replace(" ", "_"))
    travis_username = user_input("Enter your Travic-CI username", default=github_username)

    if all([project_name, fullname, github_username, github_project, travis_username]):
        return (
            project_name, fullname, github_username, github_project,
            travis_username)
    else:
        raise Exception("Cannot leave a field empty!")


def user_input(prompt, input_type=str, default=None, show_default=True, regex=None, choices=None):
    '''Continues to prompt a user for valid input until valid input has been received.'''
    if input_type not in [str, int, float, long]:
        raise TypeError("Only [str, int, float, long] types are supported")
    elif regex and not hasattr(regex, 'match'):
        raise TypeError("regex should be a compiled re object; it was a '{0:s}'".format(type(regex)))

    while True:
        if default and show_default:
            _prompt = '{0:s} [{1:s}]: '.format(prompt, str(default))
        else:
            _prompt = str(prompt)

        retval = raw_input(_prompt)

        if default and len(retval) == 0:
            retval = default

        if regex and (regex.match(retval) is None):
            print("[{0:s}] doesn't match [{1:s}]".format(retval, regex.pattern))
            continue

        if input_type is int:
            retval = int(retval)
        elif input_type is float:
            retval = float(retval)
        elif input_type is long:
            retval = long(retval)

        if choices and (retval not in choices):
            info = "[{0:s}] is not a valid choice".format(str(retval))
            print(info)
            continue

        return retval


def replace_in_file(filepath, replace_list):
    """Takes a list of replacements, applies it to the text of the file, and
    writes the result back over the file.

    """
    with open(filepath, 'rb') as fh:
        text = fh.read()

    for replace, _with in replace_list:
        text = re.sub(replace, _with, text)

    if DEBUG:
        print(text)
    else:
        with open(filepath, 'wb') as fh:
            fh.write(text)


def get_name_patch(path):
    """An OS-agnostic way of matching the patch paths with the os path."""
    if os.path.isfile(path):
        for key, function in patches["files"].items():
            if key in path:
                return function

    return None


def process(user_data, root_directory):
    for root, dirs, files in os.walk(root_directory, topdown=False):
        for name in files:
            patch = get_name_patch(os.path.join(root, name))
            if patch:
                patch(user_data, os.path.join(root, name))
        for name in dirs:
            if name in patches["dirs"]:
                patches["dirs"][name](user_data, os.path.join(root, name))


def license(user_data, filepath):
    replace_list = [
        ("CURRENTYEAR", user_data["current_year"]),
        ("FULLNAME", user_data["fullname"])
    ]
    replace_in_file(filepath, replace_list)


def proj_dir(user_data, dirpath):
    newpath = re.sub("SAMPLEPROJDIRNAME", user_data["project_dir_name"], dirpath)

    if DEBUG:
        print(newpath)
    else:
        shutil.move(dirpath, newpath)


def readme(user_data, filepath):
    replace_list = [
        ("TRAVISUSERNAME", user_data["travis_username"]),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"])
    ]
    replace_in_file(filepath, replace_list)


def auto_generate(user_data, filepath):
    replace_list = [
        ("TRAVISUSERNAME", user_data["travis_username"]),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"])
    ]
    replace_in_file(filepath, replace_list)


def conf(user_data, filepath):
    replace_list = [
        ('"SAMPLEPROJ"', '"%s"' % user_data["project_name"]),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
        ("FULLNAME", user_data["fullname"]),
        ("CURRENTYEAR", user_data["current_year"]),
    ]
    replace_in_file(filepath, replace_list)


def index_rst(user_data, filepath):
    newhead = "Documentation for %s" % user_data["project_name"]
    newtag = "=" * len(newhead)

    replace_list = [
        ("SAMPLEPROJ", user_data["project_name"]),
        ("============================", newtag)
    ]
    replace_in_file(filepath, replace_list)


def auto_rst(user_data, filepath):
    replace_list = [
        ("SAMPLEPROJ", user_data["project_name"]),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
        ("GHUSERNAME", user_data["github_username"]),
        ("GHPROJNAME", user_data["github_project_name"]),
    ]
    replace_in_file(filepath, replace_list)


def create_release(user_data, filepath):
    replace_list = [
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
    ]
    replace_in_file(filepath, replace_list)


def logger(user_data, filepath):
    replace_list = [
        ("FULLNAME", user_data["fullname"]),
        ("CURRENTYEAR", user_data["current_year"]),
        ("99/99/9999", time.strftime("%m/%d/%Y", time.localtime())),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
    ]
    replace_in_file(filepath, replace_list)


def init_py(user_data, filepath):
    replace_list = [
        ("FULLNAME", user_data["fullname"]),
        ("CURRENTYEAR", user_data["current_year"]),
        ("99/99/9999", time.strftime("%m/%d/%Y", time.localtime())),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
        ("SAMPEPROJNAME", user_data["project_name"]),
    ]
    replace_in_file(filepath, replace_list)


def manifest(user_data, filepath):
    replace_list = [
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
    ]
    replace_in_file(filepath, replace_list)


def setup_py(user_data, filepath):
    replace_list = [
        ("SAMPEPROJNAME", user_data["project_name"]),
        ("SAMPLEPROJDIRNAME", user_data["project_dir_name"]),
        ("GHUSERNAME", user_data["github_username"]),
        ("GHPROJNAME", user_data["github_project_name"]),
        ("FULLNAME", user_data["fullname"]),
    ]
    replace_in_file(filepath, replace_list)


def test_sample(user_data, filepath):
    init_py(user_data, filepath)
    newpath = re.sub("test_SAMPLEPROJDIRNAME", "test_%s" % user_data["project_dir_name"], filepath)

    if DEBUG:
        print(newpath)
    else:
        os.rename(filepath, newpath)

patches = {
    "files": {
        "LICENSE.txt": license,
        "README.md": readme,
        os.path.join("src", "MANIFEST.in"): manifest,
        os.path.join("src", "README.rst"): readme,
        os.path.join("src", "setup.py"): setup_py,
        os.path.join("docs", "auto-generate.py"): auto_generate,
        os.path.join("docs", "conf.py"): conf,
        os.path.join("docs", "index.rst"): index_rst,
        os.path.join("rst", "auto.rst"): auto_rst,
        os.path.join("rst", "intro.rst"): auto_rst,
        os.path.join("scripts", "create-release.py"): create_release,
        os.path.join("SAMPLEPROJDIRNAME", "logger.py"): logger,
        os.path.join("SAMPLEPROJDIRNAME", "__init__.py"): init_py,
        os.path.join("SAMPLEPROJDIRNAME", "__main__.py"): init_py,
        os.path.join("SAMPLEPROJDIRNAME", "tests", "test_SAMPLEPROJDIRNAME.py"): init_py,
        os.path.join("test_SAMPLEPROJDIRNAME.py"): test_sample,
    },
    "dirs": {
        "SAMPLEPROJDIRNAME": proj_dir,
    },
}

################################################################################
if __name__ == '__main__':
    print("**** WARNING: THIS PROCESS IS NOT REVERSIBLE ****")
    confirm = user_input("Enter Y to continue: ")
    if confirm.upper() != "Y":
        sys.exit()

    root_directory = os.path.join(os.path.dirname(__file__), "..")
    project_name, fullname, github_username, github_project_name, travis_username = get_user_data()
    current_year = time.strftime("%Y", time.localtime())
    user_data = {
        "project_name": project_name,
        "project_dir_name": project_name.replace(" ", "_"),
        "fullname": fullname,
        "github_username": github_username,
        "github_project_name": github_project_name,
        "travis_username": travis_username,
        "current_year": current_year
    }

    process(user_data, root_directory)

    thisfile = os.path.abspath(__file__)
    newname = "_already_used_" + os.path.basename(__file__)
    os.rename(__file__, newname)
