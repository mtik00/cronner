.. documentation for using cronner

Usage
=======

Introduction
------------

To run the script, use: ``python -m cronner --settings-file jobs.json --cache-file cache.db --log-file log.txt``
(the names of the files are just suggestions)

To see all of the command-line options, use ``python -m cronner``.  Here's
an example:

.. code::

    running [cronner] version [1.0.0dev] from [c:\Python27\Lib\site-packages\cronner]
    usage: cronner [-h] --cache-file CACHE_FILE --settings-file SETTINGS_FILE
                   --log-file LOG_FILE [--history] [--clear-last-run]

    optional arguments:
      -h, --help            show this help message and exit
      --cache-file CACHE_FILE
                            Path to the cache file
      --settings-file SETTINGS_FILE
                            Path to the settings file
      --log-file LOG_FILE   Path to the log file
      --history             Display job history
      --clear-last-run      Clears the last run of all jobs

Batch File
----------

You can run the ``python -m cronner`` command however you want.  However, you
may want to create a BATCH file to make life easier (and keep less info in the
inevitable Task Manager entry).  Here's a sample BATCH file.

.. code:: bat

    @echo off
    set cache=cache.db
    set settings=config.json
    set log=log.txt

    @echo on
    python -m cronner --cache-file %cache% --settings-file %settings% --log-file %log% %*

Recommendations
---------------

We recommend using cronner like the following (assuming you already have cronner
installed):

#.  Create a folder to contain your cronner files (e.g. ``C:\cronner-data``)
#.  Create a file named ``go.bat`` in the folder with the text above
#.  Create a sample ``config.json`` file

After that's complete, you can either run cronner manually from this directory,
or you can add a Task Manager item to run it for you.  If you use Task Manager,
don't forget set the working directory to the directory you put ``go.bat`` in.
Otherwise this won't work (your custom settings file will never be read).