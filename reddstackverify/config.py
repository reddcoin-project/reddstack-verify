#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
from .version import __version__

VERSION = __version__

DEBUG = True


def get_working_dir():
    from os.path import expanduser
    home = expanduser('~')

    working_dir = os.path.join(home, '.reddstackverify')

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def get_pid_filename():
    return 'reddstackverify'


logPath = get_working_dir()
log = logging.getLogger()
if len(log.handlers) == 0:
    log.setLevel(logging.DEBUG if DEBUG else logging.INFO)

if not os.path.isdir(logPath):
    os.makedirs(logPath)
logFileHandler = RotatingFileHandler(logPath + "/reddstack-verify.log", maxBytes=50000000, backupCount=99)
log_format = ('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] (' + str(os.getpid()) + ') %(message)s' if DEBUG else '%(message)s')
logfile_formatter = logging.Formatter(log_format)
logFileHandler.setFormatter(logfile_formatter)
log.addHandler(logFileHandler)
