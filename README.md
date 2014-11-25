[![travis ci build state](https://travis-ci.org/mtik00/cronner.svg?branch=master)](https://travis-ci.org/mtik00/cronner)

Introduction
============

Sample Python project.  I use this to create new projects.  You should change
this section to whatever you need.

Usage
=====

1.  Download/clone this repository
2.  run "initialize.py" from the script directory
3.  Answer all of the questions (you should have a Travis-CI account)

When that is done, your project should be good to go.

The alternative is to use an editor to replace all occurrences of these strings:

* `PROJECTNAME`: The *normal* name of the project; spaces are OK
* `cronner`: The directory name of the package; same as `PROJECTNAME`
    except spaces will be replaced with underscores.  This is the *importable*
    name.
* `GHUSERNAME`: Your github user name
* `GHPROJNAME`: The name of the project on github.  This is used for the URL
    to the github page.  E.g. `https://github.com/GHUSERNAME/GHPROJNAME`
* `FULLNAME`: Your full name.  E.g. "Firstname Lastname"
* `mtik00`: Your Travis-CI user name
* `CURRENTYEAR`: The current year; used for copyright information

You'll also need to rename `src/cronner` and
    `cronner/tests/test_cronner.py` accordingly.

Documentation
=============

HTML documentation is supported using Sphinx and pypandoc.  For
this to work completely, you should have those two things already installed.

Do generate HTML documentation:

* change to the `docs` folder
* `make clean && make html`

This will build the documentation in the `_build\html` folder.  I use a special
script to auto-generate the API documentation as well.  I suggest you take a
look at the docs to see if you want that feature.  If you don't like it, you
can remove the offending line from `docs\conf.py` (the script that does this is
called `auto-generate.py`).  If you add documentation for specific modules,
you'll need to add `noindex` entries where appropriate.

Documentation is also built and added to the release.

Building Releases
=================

You will find a script called `create-release.py` in the `scripts` folder.  You
can run this script to build a pip-installable tarball.  The tarball will be
placed in the `release` folder, and include your unit tests and the
documentation.
