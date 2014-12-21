.. documentation for the cache

Caching
=======

Introduction
------------

Cronner keeps track of the things it does using a Sqlite3 database.  This makes
it easier for you, the user, to see what happened and when it did.  Only advanced
users should modify the database directly.  You should let cronner make any
changes needed.

You do not need to create a database.  A new database will be created the first
time you run cronner, if needed.  You should always choose this option over
attempting to create one yourself.

Tables
------

Cronner uses 2 tables in the database.  One table holds the job information,
and the other table holds the job run history.

jobs
~~~~

The jobs table structure contains 5 columns:

* `hash` (TEXT NOT NULL UNIQUE): This contains a unique identifier for each job.  It's created from
    the text contained in the JSON dictionary.
* `description` (TEXT NOT NULL): This is from the ``description`` field in the JSON file.
* `last_run` (REAL): This is the local epoch time of the last time the job was run.
* `next_run` (REAL): This is the local epoch time of the next time the job should be run.
* `last_run_result` (INTEGER): This is the return code of the last-run job

history
~~~~~~~

The ``history`` table structure contains 4 columns:

* `hash` (TEXT): This contains a unique identifier for each job.  It's created from
    the text contained in the JSON dictionary.  This is a foreign key to the
    ``jobs`` table
* `description` (TEXT): This is from the ``description`` field in the JSON file.  This
    doesn't really need to be here; it's here mainly for debugging purposes.
* `time` (REAL): This is the local epoch time when the job was run.
* `result` (INTEGER): This is the return code of the last-run job
