.. documentation for the JSON data format

JSON Data Format
================

Introduction
------------

The configuration settings are stored in JSON format.  There's one exception:
we support comments in the form of ``//``.  Everything after ``//`` will be ignored.

You can read more about the format used by reading the Persistent Pineapple
documentation [3]_.

General Options
---------------

* `log-file-mode`: The mode passed to `open`; You probably want to use `"a"`
* `log-file-level`: The string-based logging.level for the log file (e.g. "DEBUG")
* `log-file-formatter`: See the Python documentation [1]_
* `screen-formatter`: See the Python documentation [1]_
* `vars`: Any variable expansions for the jobs (see :ref:`json_variables`)
* `jobs`: See below

.. _json_variables:

Variables
---------

Each job has the ability to include `variables` in the ``command``.  This allows
you to set environment-variable-like parameters in a common section.  This is
the ``vars`` section in the General Options.

``vars`` is a dictionary, where the keys are the text to search for in command
(w/o % symbols), and the values are what to replace the variable with.  It is
strongly recommened that you use a constant character to mark the variable.  For
example, surround the text with ``%`` (e.g. "%PYTHON%":
"c:/Python27/bin/python.exe").  This will make the expansion more likely to
succeed and not cause any problems.

The variables are case-sensitive.  "%PYTHON%" is not the same as "%python%".


Jobs
----

`jobs` is a list of dictionaries that describe each job you want to run.  Each
job can contain the following keys:

* `description`: A string description of the job
* `cron-job`: The *crontab* entry.  See Josiah Carlson's documentation [2]_
* `command`: The command you want to run
* `working-dir`: The directory you want to run the command in

.. _json_example:

Example
-------

Here's a sample configuration file:

.. code:: json

    {
        // Logging options /////////////////////////////////////////////////////////
        "log-file-mode": "a",
        "log-file-level": "DEBUG",

        // https://docs.python.org/2/library/logging.html#logrecord-attributes
        "log-file-formatter": "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        "screen-formatter": "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        ////////////////////////////////////////////////////////////////////////////

        // Variable Expansion //////////////////////////////////////////////////
        "vars": {
            "%PYTHON%": "C:/Python27/python2.7.exe"
        },

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

.. [1] https://docs.python.org/2/library/logging.html#logrecord-attributes
.. [2] https://github.com/josiahcarlson/parse-crontab
.. [3] https://github.com/JasonAUnrein/Persistent-Pineapple