# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot

import socket
import ftplib


class FTPBanner(BaseModule):
    def __init__(self):
        super(FTPBanner, self).__init__(name="FTP Banner",
                                        description="Gets the banner for the FTP server",
                                        loot_name="ftp-banner",
                                        intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Attempt to get the banner of an FTP server
        :param ip: IP to use
        :param port: Port to use
        """

        self.create_loot_space(ip, port)

        ftp_client = ftplib.FTP()
        try:
            self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
            ftp_client.connect(ip, port, timeout=15)
            self.logger.info("Successfully connected to {IP}:{PORT}".format(IP=ip, PORT=port))
            Loot.loot[ip][str(port)][self.loot_name] = ftp_client.getwelcome()\
                .replace("220-", "")\
                .replace("220 ", "")  # Get rid of FTP codes beforehand
            self.logger.info("Retrieved FTP banner from {IP}:{PORT}".format(IP=ip, PORT=port))
            ftp_client.quit()
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
        Should the FTP Banner module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(FTPBanner, self).should_execute(service, port):
            return False
        if service == "ftp":
            return True
        if port == 21:
            return True
        return False
