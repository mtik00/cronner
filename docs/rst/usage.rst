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

  running [cronner] version [1.0.0dev] from [e:\dropbox\code\python\cronner\src\cronner]
  usage: cronner [-h] --cache-file CACHE_FILE --settings-file SETTINGS_FILE
                 --log-file LOG_FILE [--history] [--clear-last-run] [--echo]
                 [--sleep-after SLEEP_AFTER]

  optional arguments:
    -h, --help            show this help message and exit
    --cache-file CACHE_FILE
                          Path to the cache file
    --settings-file SETTINGS_FILE
                          Path to the settings file
    --log-file LOG_FILE   Path to the log file
    --history             Display job history
    --clear-last-run      Clears the last run of all jobs
    --echo                Echo stdout from command
    --sleep-after SLEEP_AFTER
                          Number of seconds to wait after jobs complete before
                          sleeping (0=disabled)

Batch File
----------

You can run the ``python -m cronner`` command however you want.  However, you
may want to create a BATCH file to make life easier (and keep less info in the
inevitable Task Manager entry).  Here's a sample BATCH file.

.. code:: bat

    :: cronner BATCH file
    :: You can use this BATCH file to run cronner from a directory of your choosing.
    :: This directory should already be created, and contain at least *this* BATCH
    :: file and your settings file.  The other files will be created as needed.
    pushd "%~dp0"
    @echo off

    :: set up variables to make the command more portable.
    set cache=cache.db
    set settings=config.json
    set log=log.txt
    set sleep_time=30

    :: this command will run your config file and then sleep your computer.  The
    :: "%*" at the end allows you to override the command line.  For example, if you
    :: wanted to run cronner without sleeping, you call this script like so:
    ::    go.bat --sleep-after 0
    call python -m cronner --cache-file %cache% --settings-file %settings% --log-file %log% --echo --sleep-after %sleep_time% %*
    popd

    :: These lines will display a message in the DOS window after your computer has
    :: woken from sleep.  It's probably good to keep these in here in case anything
    :: goes wrong (otherwise you wouldn't see it).  Cronner will also tell you
    :: the next scheduled time to run the task.
    echo Welcome back
    pause

Recommendations
---------------

We recommend using cronner like the following (assuming you already have cronner
installed):

#.  Create a folder to contain your cronner files (e.g. ``C:\cronner-data``)
#.  Create a file named ``go.bat`` in the folder with the text above
#.  Create a sample ``config.json`` file (:ref:`json_example`)

After that's complete, you can either run cronner manually from this directory,
or you can add a Task Manager item to run it for you.  If you use Task Manager,
don't forget set the working directory to the directory you put ``go.bat`` in.
Otherwise this won't work (your custom settings file will never be read).

Personally, I have the batch file mapped to a custom key.  I use that key to
sleep my computer when I'm going to be away from it for a while (e.g. before
I go to work).  I simply hit the key and walk away.

Windows Service
---------------

Someday I'd really like to add a Windows service.  It wouldn't be very
difficult, as it's certainly been done before [1]_.  However, I actually enjoy
the *active* running of the script and that I get feedback of what the script
did when I power back on my PC after a sleep. **shrugs** YMMV

.. [1] http://code.activestate.com/recipes/576451-how-to-create-a-windows-service-in-python/