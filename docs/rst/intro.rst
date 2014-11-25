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
Download the `latest release tarball <https://github.com/mtik00/cronner/releases/latest>`_ and install with ``pip install <package>``.

Usage
=====

To run the script, use: ``python -m cronner jobs.json cache.db``
You can also create a script to do this for you, of course.

The cache file will be created if it doesn't already exist.

JSON Format
===========

The configuration settings are stored in JSON format.  There's one exception:
we support comments in the form of ``//``.  Everything after ``//`` will be ignored.

Cron job schedule parsing is provided through Josiah Carlson's *crontab* project.
`See the project page for more information <https://github.com/josiahcarlson/parse-crontab>`_.

The file paths for "log-file" and "cache-file" can either be absolute paths or
paths relative to where ever you run the script from.

Here's a sample configuration file:

.. code:: json

    {
        "cache-file": "cache.db",

        // Logging options /////////////////////////////////////////////////////////
        "log-file": "log.txt",
        "log-file-mode": "a",
        "log-file-level": "DEBUG",

        // https://docs.python.org/2/library/logging.html#logrecord-attributes
        "log-file-formatter": "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        "screen-formatter": "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        ////////////////////////////////////////////////////////////////////////////

        "jobs": [
            {
                "description": "glacier backup: documents",
                "cron-job": "@weekly",
                "command": "glacier-sync.exe glacier z:/documents us-west-2 documents nckhs",
                "working-dir": "c:/Program Files/FastGlacier"
            },
            {
                "description": "ccleaner",
                //           M   H   DA   MON    DOW     Y
                "cron-job": "0   0    *    *     */2     *",
                "command": "CCleaner.exe /AUTO",
                "working-dir": "C:/Program Files/CCleaner"
            }
        ]
    }
