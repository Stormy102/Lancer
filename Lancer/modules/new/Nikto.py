#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.new.BaseModule import BaseModule

import requests
import Loot
import json


class Nikto(BaseModule):
    def __init__(self):
        super(Nikto, self).__init__(name="Nikto",
                                          description="Scans the given web server",
                                          loot_name="Nikto",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)
        self.required_programs = ["nikto"]

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

    def should_execute(self, service: str, port: int) -> bool:
        if service is "http":
            return True
        if service is "ssl/https":
            return True
        if port is 80:
            return True
        if port is 8008:
            return True
        if port is 8080:
            return True
        return False
