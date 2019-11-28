# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from core import Loot

import socket


class GetHostname(BaseModule):
    def __init__(self):
        super(GetHostname, self).__init__(name="Get Hostname",
                                          description="Attempts to get a machine's hostname, as well as any other"
                                                      "aliases",
                                          loot_name="hostname",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

        self.logger.debug("Attempting to retrieve potential hostname(s) for {IP}".format(IP=ip))
        try:
            result = socket.gethostbyaddr(ip)
            Loot.loot[ip][self.loot_name]["Hostname"] = result[0]
            Loot.loot[ip][self.loot_name]["Aliases"] = result[1]
            self.logger.info("Successfully retrieved potential hostname for {IP}".format(IP=ip))
        except socket.herror:
            self.logger.error("Unable to resolve any hostnames for {IP}".format(IP=ip))

    def create_loot_space(self, ip: str, port: int):
        if ip not in Loot.loot:
            Loot.loot[ip] = {}
        if self.loot_name not in Loot.loot[ip]:
            Loot.loot[ip][self.loot_name] = {}

    def should_execute(self, service: str, port: int) -> bool:
        # Check if this module is disabled in the config.ini file
        if not super(GetHostname, self).should_execute(service, port):
            return False
        return True
