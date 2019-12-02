# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import Loot

import requests


class HTTPHeaders(GenericWebServiceModule):
    def __init__(self):
        super(HTTPHeaders, self).__init__(name="HTTP Headers",
                                          description="Pulls all of the HTTP Headers for useful information",
                                          loot_name="http-headers",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

        url = self.get_url(ip, port)

        self.logger.debug("Sending request to {URL}".format(URL=url))
        try:
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
