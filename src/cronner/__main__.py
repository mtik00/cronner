#!/usr/bin/env python
"""This module is used to provide functionality to
`python -m cronner`

By default, it will print out the module name, version, and location.
"""
from __future__ import print_function
import sys
from os import path
from .executor import execute


def init_parser():
    parser = argparse.ArgumentParser(prog="cronner")
    parser.add_argument('--cache-file', help="Path to the cache file", required=True)
    parser.add_argument('--settings-file', help="Path to the settings file", required=True)
    parser.add_argument('--log-file', help="Path to the log file", required=True)
    parser.add_argument('--history', help="Display job history", action="store_true", default=False)
    parser.add_argument('--clear-last-run', help="Clears the last run of all jobs", action="store_true", default=False)
    parser.add_argument('--echo', help="Echo stdout from command", action="store_true", default=False)
    parser.add_argument('--sleep-after', help="Number of seconds to wait after jobs complete before sleeping (0=disabled)", default=0, type=float)
    return parser


def show_history(jobs):
    """Displays all jobs and their corresponding data."""
    for job in jobs:
        print("============", job["description"])
        print("...schedule: ", job["cron-job"].schedule)
        print("...last run: %s" % time.asctime(time.localtime(job["last-run"])))
        print("......result:", job["last-run-result"])
        print("...next run: %s" % time.asctime(time.localtime(job["next-run"])))


def expand(items, vars):
    """Expands all variables in command that are in the form of %VAR% in vars.

    :param str list items: A list of strings you want to expand
    :param dict vars: A dictionary where the keys are the variables, and the
        values are the result of the expansion.
    """
    # This algorithm is a little inefficient since we loop through vars as
    # opposed to something like `while %XXX% in command`.  This is so we don't
    # mess around with any 'true' environment variables.  vars is probably going
    # to be a small dictionary anyway, so it's not too bad.  This also makes
    # a dead-simple loop exit, and we don't have to worry about users using
    # some other marking character.
    result = []
    for item in items:
        for variable, value in vars.items():
            if variable in item:
                item = item.replace(variable, value)

        result.append(item)

    return result


def process(jobs, vars, echo=False):
    """Perform each job command (if needed)."""
    logger.debug("=========================================== Starting process")
    for job in jobs:
        run = False
        item = cache.get(job["id"])

        if item and (item["last-run-result"]):
            print("<%s> failed last time; running it again" % item["description"])
            run = True
        elif item and (not item["last-run"]):
            print("<%s> never ran" % item["description"])
            run = True
        elif item and (time.time() > item["next-run"]):
            print("time to run <%s>" % item["description"])
            run = True

        if run:
            print("running <%s>" % job["description"])

            command, working_dir = expand((job["command"], job["working-dir"]), vars)
            returncode, stdout = execute(
                command, working_dir=working_dir, echo=echo, echo_indent=4)

            logger.debug(
                "[%s] in [%s] returned: [%i: %s]", command,
                working_dir, returncode, stdout.strip())

            job["last-run"] = time.time()
            job["next-run"] = job["cron-job"].next_time()
            job["last-run-result"] = returncode
            cache.update(job)
            cache.add_result(job)
        else:
            log = "not time to run <%s> (next run on %s)" % (
                job["description"], job["cron-job"].next_time(asc=True))
            print(log)
            logger.debug(log)


def clear_last_run(jobs, cache):
    for job in jobs:
        job["last-run"] = 0
        cache.update(job)


if __name__ == '__main__':
    import os
    import time
    import argparse

    # Read the version from our project
    this_directory = path.abspath(path.dirname(__file__))
    package_dir = path.join(this_directory, "..")
    sys.path.insert(0, package_dir)
    from . import __version__

    parser = init_parser()
    if len(sys.argv) == 1:
        print("running [{0}] version [{1}] from [{2}]".format(
              "cronner", __version__, this_directory))

        parser.print_help()

        sys.exit()

    from .settings import get_settings
    from .logger import get_logger
    from .cache import get_cache
    from .mycrontab import CronTab

    args = parser.parse_args()

    settings = get_settings(args.settings_file)
    logger = get_logger(logfile=args.log_file)
    cache = get_cache(os.path.join(args.cache_file))
    crontab = CronTab(settings.get("jobs"))

    if args.history:
        show_history(crontab.jobs)
    elif args.clear_last_run:
        clear_last_run(crontab.jobs, cache)
    else:
        try:
            vars = settings.get("vars")
        except:
            vars = {}

        process(crontab.jobs, vars, args.echo)

        if args.sleep_after:
            from .sleeper import sleep_pc

            print("Sleeping after {0} seconds".format(args.sleep_after))
            time.sleep(args.sleep_after)
            sleep_pc()
