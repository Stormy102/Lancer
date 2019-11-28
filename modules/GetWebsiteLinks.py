# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from core import Loot

import requests


class GetWebsiteLinks(BaseModule):

    def __init__(self):
        super(GetWebsiteLinks, self).__init__(name="Get Website Links",
                                              description="Scrapes all of the internal and external links from a"
                                                          " website",
                                              loot_name="links",
                                              multithreaded=False,
                                              intrusive=False,
                                              critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

        Loot.loot[ip][str(port)][self.loot_name]["Internal"] = []
        Loot.loot[ip][str(port)][self.loot_name]["External"] = []

        if port == 443:
            url = "https://{IP}".format(IP=ip)
        elif port == 80:
            url = "http://{IP}".format(IP=ip)
        else:
            url = "http://{IP}:{PORT}".format(IP=ip, PORT=port)

        try:
            response = requests.get(url, allow_redirects=True)

            for link in BeautifulSoup(response.text, features="html.parser", parse_only=SoupStrainer('a')):
                if hasattr(link, 'href'):
                    parse = urlparse(link['href'])
                    loot_url = parse[1] + parse[2]
                    if self.is_internal_url(ip, parse[1]):
                        self.logger.debug("{URL} is an internal URL".format(URL=loot_url))
                        Loot.loot[ip][str(port)][self.loot_name]["Internal"].append(loot_url)
                    else:
                        self.logger.debug("{URL} is an external URL".format(URL=loot_url))
                        Loot.loot[ip][str(port)][self.loot_name]["External"].append(loot_url)

            self.logger.info("Found {INTERNAL} internal links and {EXTERNAL} external links"
                             .format(INTERNAL=len(Loot.loot[ip][str(port)][self.loot_name]["Internal"]),
                                     EXTERNAL=len(Loot.loot[ip][str(port)][self.loot_name]["External"])))
        except requests.exceptions.ConnectionError:
            self.logger.error("Unable to connect to {URL}".format(URL=url))

    def is_internal_url(self, base_url, url) -> bool:
        if url != "":
            self.logger.debug("Checking if {URL} is an internal URL to {BASE}".format(URL=url, BASE=base_url))
        if url == "":
            return True
        if base_url in url:
            return True
        return False

    def should_execute(self, service: str, port: int) -> bool:
        # Check if this module is disabled in the config.ini file
        if not super(GetWebsiteLinks, self).should_execute(service, port):
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
