# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.config import get_logger


class Report(object):

    def __init__(self, name: str):
        self.name = name

        self.logger = get_logger(name)

        self.logger.debug("Created {NAME} report instance".format(NAME=name))

    def generate_report(self, data: dict) -> None:
        pass
