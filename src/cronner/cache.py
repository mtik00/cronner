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
    global CACHE
    CACHE = Cache(cache_file)


def get_cache(config_file=None):
    if CACHE is None:
        _init(config_file)

    return CACHE


class Cache:
    def __init__(self, cache_file):
        self.filename = cache_file

        if not os.path.isfile(self.filename):
            self._create()

        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()

    def __del__(self):
        if getattr(self, "conn", None):
            self.conn.commit()
            self.conn.close()

    def _create(self):
        self.cur.execute('''
            CREATE TABLE history
            (hash text, description text, time real, result integer)''')

        self.cur.execute('''
            CREATE TABLE jobs
            (hash text not null unique primary key, description text not null,
             last_run real, next_run real, last_run_result integer)''')

    def has(self, job):
        return bool(self.get(job["id"]))

    def get(self, id):
        cmd = "SELECT * FROM jobs WHERE hash=?"
        self.cur.execute(cmd, (id,))
        item = self.cur.fetchone()
        if item:
            return dict(zip(
                ("id", "description", "last-run", "next-run", "last-run-result"),
                item))

        return None

    def update(self, job):
        cmd = "UPDATE jobs SET last_run=?,next_run=?,last_run_result=? WHERE hash=?"
        self.cur.execute(cmd, (
            job["last-run"], job["next-run"], job["last-run-result"], job["id"]))

    def add_job(self, job):
        cmd = "INSERT INTO jobs(hash,description,last_run,next_run,last_run_result) VALUES(?,?,?,?,?)"
        self.cur.execute(
            cmd,
            (job["id"], job["description"], job["last-run"], job["next-run"], job["last-run-result"]))

        return True

    def add_result(self, job):
        cmd = "INSERT INTO history(hash,description,time,result) VALUES(?,?,?,?)"
        self.cur.execute(
            cmd,
            (job["id"], job["description"], job["last-run"], job["last-run-result"]))

        return True
