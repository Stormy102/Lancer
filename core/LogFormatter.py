# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

    This is the config module.
    This holds all of the key information which should be accessed globally across Lancer.
"""

from core import utils

import logging


class LogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord):
        if record.levelno == logging.WARNING:
            return utils.warning_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
        if record.levelno >= logging.ERROR:
            return utils.error_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
        return utils.normal_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
