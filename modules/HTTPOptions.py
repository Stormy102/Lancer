# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from core import Loot

import http.client
import socket


class HTTPOptions(BaseModule):

    def __init__(self):
        super(HTTPOptions, self).__init__(name="HTTP Options",
                                          description="Checks the HTTP Options available for a server",
                                          loot_name="http-options",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)
        Loot.loot[ip][str(port)][self.loot_name] = []

        try:
            self.logger.debug("Sending HTTP connection request to {IP}:{PORT}".format(IP=ip, PORT=port))
            conn = http.client.HTTPConnection(ip, port, timeout=10)
            conn.request('OPTIONS', '/')  # '/dist/httpd/')
            response = conn.getresponse()
            conn.close()
            self.logger.debug("Received response from {IP}:{PORT}".format(IP=ip, PORT=port))
            allowed = response.getheader('allow')
            if allowed:
                Loot.loot[ip][str(port)][self.loot_name] = allowed.split(",")
                self.logger.info("Server responded to OPTIONS: {OPTIONS}".format(OPTIONS=allowed))
            else:
                self.logger.info("OPTIONS HTTP verb not allowed for {URL}".format(URL=ip))
        except http.client.BadStatusLine:
            self.logger.error("Unable to parse HTTP status line")
        except socket.error:
            self.logger.error("Socket Error occurred")

    def should_execute(self, service: str, port: int) -> bool:
        # Check if this module is disabled in the config.ini file
        if not super(HTTPOptions, self).should_execute(service, port):
            return False
        if service == "http":
            return True
        if service == "ssl/https":
            return True
        if service == "http-proxy":
            return True
        if service == "https-alt":
            return True
        if port == 80:
            return True
        if port == 443:
            return True
        if port == 8080:
            return True
        if port == 8008:
            return True
        if port == 8443:
            return True
        return False
