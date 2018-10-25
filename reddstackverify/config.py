#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
from .version import __version__

VERSION = __version__

DEBUG = True
logPath = "../logs"
log = logging.getLogger()
if len(log.handlers) == 0:
	logPath = "../logs"
	if not os.path.isdir(logPath):
	    os.makedirs(logPath)
	logFileHandler = RotatingFileHandler(logPath + "/reddstack-verify.log", maxBytes=50000000, backupCount=99)
	log_format = ('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] (' + str(os.getpid()) + ') %(message)s' if DEBUG else '%(message)s')
	logfile_formatter = logging.Formatter(log_format)
	logFileHandler.setFormatter(logfile_formatter)
	log.addHandler(logFileHandler)