# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot, config

import socket
import telnetlib


class TelnetBanner(BaseModule):
    def __init__(self):
        super(TelnetBanner, self).__init__(name="Telnet Banner",
                                           description="Gets the banner for the Telnet server",
                                           loot_name="telnet-banner",
                                           intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Attempt to get the banner of an Telnet server
        :param ip: IP to use
        :param port: Port to use
        """

        self.create_loot_space(ip, port)

        telnet = telnetlib.Telnet()
        try:
            self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
            telnet.open(ip, port, config.get_timeout())
            self.logger.info("Successfully connected to {IP}:{PORT}".format(IP=ip, PORT=port))
            raw_banner = telnet.read_until(b"login:", 15).decode("UTF-8")
            if "login:" in raw_banner:
                raw_banner = raw_banner.replace("login:", "")
            if "password:" in raw_banner:
                raw_banner = raw_banner.replace("password:", "")
            if "username:" in raw_banner:
                raw_banner = raw_banner.replace("username:", "")

            banner = ""
            for line in raw_banner.splitlines():
                if line:
                    banner += line

            Loot.loot[ip][str(port)][self.loot_name] = banner
            self.logger.info("Retrieved FTP banner from {IP}:{PORT}".format(IP=ip, PORT=port))
            telnet.close()
            self.logger.debug("Disconnected from {IP}:{PORT}".format(IP=ip, PORT=port))
        except socket.gaierror:
            # Log of some kind
            self.logger.error("Failed to connect: Invalid IP Address/Hostname")
        except ConnectionRefusedError:
            # Log of some kind
            self.logger.error("Failed to connect: Connection refused")
        except (TimeoutError, socket.timeout):
            # Log of some kind
            self.logger.error("Failed to connect: Connection timed out")

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the Telnet Banner module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(TelnetBanner, self).should_execute(service, port):
            return False
        if "telnet" in service:
            return True
        if port == 23:
            return True
        return False
