# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from core import Loot, config

import os
import requests


class GetWebsiteLinks(GenericWebServiceModule):

    def __init__(self):
        super(GetWebsiteLinks, self).__init__(name="Get Website Links",
                                              description="Scrapes all of the internal and external links from a"
                                                          " website",
                                              loot_name="links",
                                              intrusion_level=2)

    def execute(self, ip: str, port: int) -> None:
        """
        Get all of the webpage links (non recursive for now)
        :param ip: IP to use
        :param port: Port to use
        :return:
        """

        self.create_loot_space(ip, port)

        Loot.loot[ip][str(port)][self.loot_name]["Internal"] = []
        Loot.loot[ip][str(port)][self.loot_name]["External"] = []

        url = self.get_url(ip, port)

        try:
            response = requests.get(url, allow_redirects=True)

            for link in BeautifulSoup(response.text, features="html.parser", parse_only=SoupStrainer('a')):
                if link.has_attr('href'):
                    parse = urlparse(link['href'])
                    loot_url = parse[1] + parse[2]
                    if "@" in loot_url:
                        continue
                    if loot_url == "./":
                        continue
                    if self.is_internal_url(ip, parse[1]):
                        self.log_internal_url(ip, port, loot_url)
                    else:
                        self.log_external_url(ip, port, loot_url)

            self.logger.info("Found {INTERNAL} internal links and {EXTERNAL} external links"
                             .format(INTERNAL=len(Loot.loot[ip][str(port)][self.loot_name]["Internal"]),
                                     EXTERNAL=len(Loot.loot[ip][str(port)][self.loot_name]["External"])))
        except requests.exceptions.ConnectionError:
            self.logger.error("Unable to connect to {URL}".format(URL=url))

    def log_internal_url(self, ip: str, port: int, loot_url: str) -> None:
        """
        Adds an internal URL to the dictionary and avoids duplication
        :param ip: IP
        :param port: Port
        :param loot_url: Loot URL to store
        """
        # Check that the URL isn't a duplicate
        if loot_url not in Loot.loot[ip][str(port)][self.loot_name]["Internal"]:
            self.logger.debug("{URL} is an internal URL".format(URL=loot_url))
            Loot.loot[ip][str(port)][self.loot_name]["Internal"].append(loot_url)

            with open(os.path.join(config.get_module_cache(self.name, ip, str(port)), "internal.txt"),"a") as file:
                file.write("{URL}\n".format(URL=loot_url))
        # else:
        #    self.logger.debug("Internal URL {URL} has already been seen".format(URL=loot_url))

    def log_external_url(self, ip: str, port: int, loot_url: str) -> None:
        """
        Adds an external URL to the dictionary and avoids duplication
        :param ip: IP
        :param port: Port
        :param loot_url: Loot URL to store
        """
        # Check that the URL isn't a duplicate
        if loot_url not in Loot.loot[ip][str(port)][self.loot_name]["External"]:
            self.logger.debug("{URL} is an external URL".format(URL=loot_url))
            Loot.loot[ip][str(port)][self.loot_name]["External"].append(loot_url)

            with open(os.path.join(config.get_module_cache(self.name, ip, str(port)), "external.txt"), "a") as file:
                file.write("{URL}\n".format(URL=loot_url))
        # else:
        #    self.logger.debug("External URL {URL} has already been seen".format(URL=loot_url))

    def is_internal_url(self, base_url, url) -> bool:
        """
        Checks if the URL is internal
        :param base_url: The base URL we are analysing
        :param url: The URL to check if it is internal or not
        :return: True if the URL is internal, false if not
        """
        if url != "":
            self.logger.debug("Checking if {URL} is an internal URL to {BASE}".format(URL=url, BASE=base_url))
        if url == "":
            return True
        if base_url in url:
            return True
        return False
