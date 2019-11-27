# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from core import Loot

import requests
import logging


class HTTPHeaders(BaseModule):
    def __init__(self):
        super(HTTPHeaders, self).__init__(name="HTTP Headers",
                                          description="Pulls all of the HTTP Headers for useful information",
                                          loot_name="http-headers",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

        if port == 443:
            url = "https://{IP}".format(IP=ip)
        elif port == 80:
            url = "http://{IP}".format(IP=ip)
        else:
            url = "http://{IP}:{PORT}".format(IP=ip, PORT=port)

        self.logger.debug("Sending request to {URL}".format(URL=url))
        try:
            # Suppress the DEBUG output from the urllib3.connectionpool
            logging.getLogger("urllib3").setLevel(logging.WARNING)

            response = requests.head(url, allow_redirects=True)
            Loot.loot[ip][str(port)][self.loot_name] = dict(response.headers)

            if len(response.history) > 0:
                self.logger.info("Redirected from {ORIG} to {URL}"
                                 .format(ORIG=response.history[0].url, URL=response.url))

            self.logger.info("Successfully retrieved HTTP headers")
            if "server" in response.headers:
                self.logger.info("Server header present: {SERVER}".format(SERVER=response.headers["server"]))
        except requests.exceptions.ConnectionError:
            self.logger.error("Unable to connect to {URL}".format(URL=url))

    def should_execute(self, service: str, port: int) -> bool:
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
