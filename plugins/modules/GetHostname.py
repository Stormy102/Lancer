# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot, config

import socket
import os


class GetHostname(BaseModule):
    def __init__(self):
        super(GetHostname, self).__init__(name="Get Hostname",
                                          description="Attempts to get a machine's hostname, as well as any other"
                                                      " aliases",
                                          loot_name="hostname",
                                          intrusion_level=1)

    def execute(self, ip: str, port: int) -> None:
        """
        Attempt to get the hostname of the target computer via it's IP address
        :param ip: IP to use
        :param port: Port to use
        """

        self.create_loot_space(ip, port)

        self.logger.debug("Attempting to retrieve potential hostname(s) for {IP}".format(IP=ip))
        try:
            result = socket.gethostbyaddr(ip)
            Loot.loot[ip][self.loot_name]["Hostname"] = result[0]
            Loot.loot[ip][self.loot_name]["Aliases"] = result[1]

            with open(os.path.join(config.get_current_target_cache(ip), "hostname.txt"), "w") as file:
                file.write("Hostname: {HOST}\n".format(HOST=result[0]))
                aliases = " ".join(result[1])
                if not aliases:
                    aliases = "No results"
                file.write("Aliases: {HOST}".format(HOST=aliases))

            self.logger.info("Successfully retrieved potential hostname for {IP}".format(IP=ip))
        except socket.herror:
            self.logger.error("Unable to resolve any hostnames for {IP}".format(IP=ip))

    def create_loot_space(self, ip: str, port: int):
        """
        Create a loot space in the dictionary
        :param ip: The IP to use
        :param port:  The port to use
        """

        if ip not in Loot.loot:
            Loot.loot[ip] = {}
        if self.loot_name not in Loot.loot[ip]:
            Loot.loot[ip][self.loot_name] = {}

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the Get Hostname module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        if not super(GetHostname, self).should_execute(service, port):
            return False
        if port == 0:
            return True
        return False
