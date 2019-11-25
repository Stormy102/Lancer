# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.InvalidTarget import InvalidTarget
from core import utils

import socket
import time


class Target(object):

    def __init__(self, target: str):
        try:
            socket.gethostbyname(target)
        except socket.gaierror:
            raise InvalidTarget(target + " is not a valid hostname or IPv4 address")

        print()

        self.target = target
        self.start_time = time.monotonic()
        self.finish_time = None
        self.elapsed_time = None
        self.time_taken = None
        # TODO: Use hostname if module allows it
        self.ip = socket.gethostbyname(target)
        print(utils.normal_message(), "Starting analysis of", self.target, "(" + self.ip + ")...")

    def stop_timer(self):
        self.finish_time = time.monotonic()
        self.elapsed_time = self.finish_time - self.start_time
        self.time_taken = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))

        print(utils.normal_message(), "Finished analysis of", self.target, "(" + self.ip + ")...")
        print(utils.normal_message(), "Analysis of", self.target, "took", self.time_taken)
