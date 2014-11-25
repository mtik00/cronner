#!/usr/bin/env python
"""
This module implements the caching interface for the application.
"""
# Imports ######################################################################
from __future__ import print_function
import os
import sqlite3


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
CACHE = None


def _init(cache_file):
    """Creates a new Cache object."""
    global CACHE
    CACHE = Cache(cache_file)


def get_cache(config_file=None):
    """Used to retrieve the global cache object."""
    if CACHE is None:
        _init(config_file)

    return CACHE


class Cache:
    """This object is used to interface with the job cache.  It uses a SQLite3
    database to store the information.

    :param str cache_file: The path to the cache file.  This will be created if
        it does not already exist.
    """
    def __init__(self, cache_file):
        self.filename = cache_file

        if not os.path.isfile(self.filename):
            self._create()

        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()

    def __del__(self):
        """Commit the changes and close the connection."""
        if getattr(self, "conn", None):
            self.conn.commit()
            self.conn.close()

    def _create(self):
        """Create the tables needed to store the information."""
        self.cur.execute('''
            CREATE TABLE history
            (hash text, description text, time real, result integer)''')

        self.cur.execute('''
            CREATE TABLE jobs
            (hash text not null unique primary key, description text not null,
             last_run real, next_run real, last_run_result integer)''')

    def has(self, job):
        """Checks to see whether or not a job exists in the table.

        :param dict job: The job dictionary

        :returns: True if the job exists, False otherwise
        """
        return bool(self.get(job["id"]))

    def get(self, id):
        """Retrieves the job with the selected ID.

        :param str id: The ID of the job

        :returns: The dictionary of the job if found, None otherwise
        """
        cmd = "SELECT * FROM jobs WHERE hash=?"
        self.cur.execute(cmd, (id,))
        item = self.cur.fetchone()
        if item:
            return dict(zip(
                ("id", "description", "last-run", "next-run", "last-run-result"),
                item))

        return None

    def update(self, job):
        """Update last_run, next_run, and last_run_result for an existing job.

        :param dict job: The job dictionary

        :returns: True
        """
        cmd = "UPDATE jobs SET last_run=?,next_run=?,last_run_result=? WHERE hash=?"
        self.cur.execute(cmd, (
            job["last-run"], job["next-run"], job["last-run-result"], job["id"]))

    def add_job(self, job):
        """Adds a new job into the cache.

        :param dict job: The job dictionary

        :returns: True
        """
        cmd = "INSERT INTO jobs(hash,description,last_run,next_run,last_run_result) VALUES(?,?,?,?,?)"
        self.cur.execute(
            cmd,
            (job["id"], job["description"], job["last-run"], job["next-run"], job["last-run-result"]))

        return True

    def add_result(self, job):
        """Adds a job run result to the history table.

        :param dict job: The job dictionary

        :returns: True
        """
        cmd = "INSERT INTO history(hash,description,time,result) VALUES(?,?,?,?)"
        self.cur.execute(
            cmd,
            (job["id"], job["description"], job["last-run"], job["last-run-result"]))

        return True
