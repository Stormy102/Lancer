# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule

import requests
from core import Loot
import json


class GeolocateIP(BaseModule):
    def __init__(self):
        super(GeolocateIP, self).__init__(name="Geolocate IP",
                                          description="Geolocates a given IP or DNS name",
                                          loot_name="geo",
                                          multithreaded=False,
                                          intrusive=False,
                                          critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)
        self.logger.debug("Contacting tools.keycdn.com for target geolocation information")
        response = requests.get("https://tools.keycdn.com/geo.json?host={HOST}".format(HOST=ip))
        self.logger.debug("Successfully retrieved target information")
        data = json.loads(response.text)
        geo_info = data["data"]["geo"]
        Loot.loot[ip][self.loot_name] = geo_info

    def create_loot_space(self, ip: str, port: int):
        if ip not in Loot.loot:
            Loot.loot[ip] = {}
        if self.loot_name not in Loot.loot[ip]:
            Loot.loot[ip][self.loot_name] = {}

    def should_execute(self, service: str, port: int) -> bool:
        # Check if this module is disabled in the config.ini file
        if not super(GeolocateIP, self).should_execute(service, port):
            return False
        return True
