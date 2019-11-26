# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import utils

import time
import ipaddress


class Target(object):

    def __init__(self, hostname: str, ip: ipaddress.ip_address):

        self.hostname = hostname
        self.start_time = time.monotonic()
        self.finish_time = None
        self.elapsed_time = None
        self.time_taken = None
        # TODO: Use hostname if module allows it
        self.ip = ip
        if hostname is None:
            print(utils.normal_message(), "Starting analysis of {IP}...".format(IP=self.ip))
        else:
            print(utils.normal_message(), "Starting analysis of {HOST} ({IP})..."
                  .format(HOST=self.hostname, IP=self.ip))

    def stop_timer(self):
        self.finish_time = time.monotonic()
        self.elapsed_time = self.finish_time - self.start_time
        self.time_taken = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))

        if self.hostname is None:
            print(utils.normal_message(), "Finished analysis of {IP}".format(IP=self.ip))
            print(utils.normal_message(), "Analysis of {IP} took {TIME}".format(IP=self.ip, TIME=self.time_taken))
        else:
            print(utils.normal_message(), "Finished analysis of {HOST} ({IP})".format(HOST=self.hostname, IP=self.ip))
            print(utils.normal_message(), "Analysis of {TARGET} took {TIME}"
                  .format(TARGET=self.hostname, TIME=self.time_taken))

    def get_address(self) -> str:
        if self.hostname is None:
            return str(self.ip)
        return self.hostname
