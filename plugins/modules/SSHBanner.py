# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.SSHModule import SSHModule
from core import Loot, config

import socket


class SSHBanner(SSHModule):
    def __init__(self):
        super(SSHBanner, self).__init__(name="SSH Banner",
                                        description="Gets the banner for the SSH server",
                                        loot_name="ssh-banner",
                                        intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Attempt to get the banner of a SSH server
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)

        sock = socket.socket()
        sock.settimeout(config.get_timeout())

        try:
            self.logger.debug("Connecting to {IP}:{PORT}".format(IP=ip, PORT=port))
            sock.connect((ip, port))
            self.logger.info("Successfully connected to {IP}:{PORT}".format(IP=ip, PORT=port))
            banner = sock.recv(1024).decode("UTF-8")
            self.logger.info("Retrieved SSH banner from {IP}:{PORT}".format(IP=ip, PORT=port))
            Loot.loot[ip][str(port)][self.loot_name] = banner
            sock.close()
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
