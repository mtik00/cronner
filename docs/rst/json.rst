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
* `jobs`: See below

Jobs
----

`jobs` is a list of dictionaries that describe each job you want to run.  Each
job can contain the following keys:

* `description`: A string description of the job
* `cron-job`: The *crontab* entry.  See Josiah Carlson's documentation [2]_
* `command`: The command you want to run
* `working-dir`: The directory you want to run the command in

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