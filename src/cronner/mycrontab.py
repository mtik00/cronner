#!/usr/bin/env python2.7
"""
This script is used to do something really cool
"""

# Imports ######################################################################
from __future__ import print_function
import md5
import time
from .external.crontab import CronTab as _CronTab
from .cache import get_cache
# from .persistent_pineapple import PersistentPineapple

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "01/01/2014"
__license__ = "MIT"
__version__ = "0.01"

# Globals ######################################################################
DEBUG = False


class CronTabItem(_CronTab):
    def __init__(self, cronschedule):
        self.__schedule = cronschedule
        super(CronTabItem, self).__init__(cronschedule)

    @property
    def schedule(self):
        return self.__schedule

    def next_time(self, asc=False):
        _time = time.localtime(time.time() + self.next())

        if asc:
            return time.asctime(_time)

        return time.mktime(_time)


class CronTab(object):
    def __init__(self, jobs):
        cache = get_cache()
        self.jobs = []

        for job in jobs:
            m = md5.new()
            m.update(job["description"])
            m.update(job["command"])
            m.update(job["cron-job"])
            job["id"] = m.hexdigest()
            job["cron-job"] = CronTabItem(job["cron-job"])
            job["next-run"] = job["cron-job"].next_time()

            cached = cache.get(job["id"])
            if cached:
                job["last-run"] = cached["last-run"]
                job["last-run-result"] = cached["last-run-result"]
            else:
                job["last-run"] = 0
                job["last-run-result"] = 0
                cache.add_job(job)

            self.jobs.append(job)
