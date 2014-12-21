Introduction
============

This project is a simple replacement for the Windows Task Scheduler.  It's
pure Python, so there's no reason you *couldn't* use it on Linux, but there
isn't much of a point to that.

The basic principle is that cron jobs and settings are stored in a JSON text
file.  This file is read, processed, and the results are stored each time you
run the script.

Previous runs and results are stored in an SQLite database (which we call the
cache).  The script loads the cache and figures out whether or not a cron job
should run based on the cron settings and the previous run.  There is currently
no service that runs in the background.  You'll need to run the script each time
you want to check the jobs.  In other words, "run every minute" jobs are probably
not want you want to use this for (although there's nothing stopping you from
doing so).

The project is hosted on GitHub at https://github.com/mtik00/cronner

Install
=======

Releases are uploaded to pypi.  You can install the latest release with ``pip install cronner``.

You can also download the `latest release tarball <https://github.com/mtik00/cronner/releases/latest>`_ and install with ``pip install <tarball>``.

Usage
=====

To run the script, use: ``python -m cronner --settings-file jobs.json --cache-file cache.db --log-file log.txt``

You can also create a script to do this for you, of course.  Here's a sample `go.bat`
that you can run in the same directory as the data files:

.. code:: bat

    @echo off
    set cache=cache.db
    set settings=config.json
    set log=log.txt

    @echo on
    python -m cronner --cache-file %cache% --settings-file %settings% --log-file %log% %*

The cache file will be created if it doesn't already exist.