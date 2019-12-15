# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import Loot

import http.client
import socket


class HTTPOptions(GenericWebServiceModule):

    def __init__(self):
        super(HTTPOptions, self).__init__(name="HTTP Options",
                                          description="Checks the HTTP Options available for a web server",
                                          loot_name="http-options",
                                          intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Gets the available HTTP options from the web server
        :param ip: IP to use
        :param port: Port to use
        """

        self.create_loot_space(ip, port)
        Loot.loot[ip][str(port)][self.loot_name] = []

        try:
            self.logger.debug("Sending HTTP connection request to {IP}:{PORT}".format(IP=ip, PORT=port))
            conn = http.client.HTTPConnection(ip, port, timeout=10)
            conn.request('OPTIONS', '/')
            response = conn.getresponse()
            conn.close()
            self.logger.debug("Received response from {IP}:{PORT}".format(IP=ip, PORT=port))
            allowed = response.getheader('allow')
            if allowed:
                Loot.loot[ip][str(port)][self.loot_name] = allowed.split(", ")
                self.logger.info("Server responded to OPTIONS: {OPTIONS}".format(OPTIONS=allowed))
            else:
                self.logger.info("OPTIONS HTTP verb not allowed for {URL}".format(URL=ip))
                # TODO: Brute Force different options
        # except http.client.BadStatusLine:
        #     self.logger.error("Unable to parse HTTP status line")
        except socket.error:
            self.logger.error("Socket Error occurred")
