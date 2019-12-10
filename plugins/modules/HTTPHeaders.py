# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import Loot, config

import requests
import os


class HTTPHeaders(GenericWebServiceModule):
    def __init__(self):
        super(HTTPHeaders, self).__init__(name="HTTP Headers",
                                          description="Pulls all of the HTTP Headers for useful information",
                                          loot_name="http-headers",
                                          intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Get the HTTP headers from the default webpage
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)

        url = self.get_url(ip, port)

        self.logger.debug("Sending request to {URL}".format(URL=url))
        try:
            response = requests.head(url, allow_redirects=True)

            headers = dict(response.headers)

            Loot.loot[ip][str(port)][self.loot_name] = headers

            if len(response.history) > 0:
                self.logger.info("Redirected from {ORIG} to {URL}"
                                 .format(ORIG=response.history[0].url, URL=response.url))

            self.logger.info("Successfully retrieved HTTP headers")
            if "Server" in headers:
                self.logger.info("Server header present: {SERVER}".format(SERVER=headers["Server"]))
            if "X-Powered-By" in response.headers:
                self.logger.info("Powered-By header present: {POWERED_BY}".format(POWERED_BY=headers["X-Powered-By"]))

            with open(os.path.join(config.get_module_cache(self.name, ip, str(port)), "headers.txt"), "w") \
                    as file:
                for item in dict(response.headers):
                    file.write("{KEY}: {VALUE}\n".format(KEY=item, VALUE=response.headers[item]))

        except requests.exceptions.ConnectionError:
            self.logger.error("Unable to connect to {URL}".format(URL=url))
