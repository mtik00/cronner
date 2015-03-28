Introduction
============

This project is a simple replacement for the Windows Task Scheduler.  It's
pure Python (except for ``sleep``), so there's no reason you *couldn't* use it
on Linux, but there isn't much of a point to that.

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

~~Releases are uploaded to pypi.  You can install the latest release with ``pip install cronner``.~~

You can also download the `latest release tarball <https://github.com/mtik00/cronner/releases/latest>`_ and install with ``pip install <tarball>``.
