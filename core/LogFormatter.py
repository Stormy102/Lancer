# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

    This is the config module.
    This holds all of the key information which should be accessed globally across Lancer.
"""

import logging


class LogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord):
        # TODO: Fix cyclic imports - this will probably come back and bite us in the arse
        from core.utils import warning_message, error_message, normal_message
        from core.ArgHandler import get_verbose, get_very_verbose

        if record.levelno == logging.WARNING:
            if get_verbose() or get_very_verbose():
                return warning_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
            else:
                return warning_message() + ' {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
        if record.levelno >= logging.ERROR:
            return error_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
        return normal_message() + ' [{NAME}] {MESSAGE}'.format(NAME=record.name, MESSAGE=record.getMessage())
