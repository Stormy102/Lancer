# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot, config

import requests
import os
import json


class GeolocateIP(BaseModule):
    def __init__(self):
        super(GeolocateIP, self).__init__(name="Geolocate IP",
                                          description="Geolocates a given IP or DNS name",
                                          loot_name="geo",
                                          intrusion_level=1)

    def execute(self, ip: str, port: int) -> None:
        """
        Attempt to get the geolocation of the IP address
        :param ip: IP to use
        :param port: Port to use
        """

        self.create_loot_space(ip, port)
        self.logger.debug("Contacting tools.keycdn.com for target geolocation information")
        response = requests.get("https://tools.keycdn.com/geo.json?host={HOST}".format(HOST=ip))
        self.logger.debug("Successfully retrieved target information")
        data = json.loads(response.text)
        geo_info = data["data"]["geo"]

        with open(os.path.join(config.get_current_target_cache(ip), "geolocate.txt"), "w") as file:
            for entry in geo_info:
                if geo_info[entry]:
                    file.write("{KEY}: {VALUE}\n".format(KEY=entry, VALUE=geo_info[entry]))
                else:
                    file.write("{KEY}: No results\n".format(KEY=entry))

        Loot.loot[ip][self.loot_name] = geo_info

    def create_loot_space(self, ip: str, port: int):
        """
        Create a loot space in the dictionary
        :param ip: The IP to use
        :param port:  The port to use
        """

        if ip not in Loot.loot:
            Loot.loot[ip] = {}
        if self.loot_name not in Loot.loot[ip]:
            Loot.loot[ip][self.loot_name] = {}

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the Geolocate IP module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """

        if not super(GeolocateIP, self).should_execute(service, port):
            return False
        if port == 0:
            return True
        return False
