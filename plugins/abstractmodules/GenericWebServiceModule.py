# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

#  -*- coding: utf-8 -*-
#
#  """
#      Copyright (c) 2019 Lancer developers
#      See the file 'LICENCE' for copying permissions
#  """
#

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot

import requests


class GenericWebServiceModule(BaseModule):
    def __init__(self, name: str, description: str, loot_name: str, intrusion_level: int, critical: bool = False):
        super(GenericWebServiceModule, self).__init__(name=name,
                                                      description=description,
                                                      loot_name=loot_name,
                                                      critical=critical,
                                                      intrusion_level=intrusion_level)

    # noinspection PyMethodMayBeStatic
    def get_url(self, ip: str, port: int) -> str:
        """
        Get the IP/Hostname and port as a HTTP/HTTPS string. Useful for web requests/enumeration
        :param ip: The IP or hostname
        :param port: The port to use in the URL
        :return: Returns the correctly formatted string prefixed with the correct protocol
        """
        if port == 443:
            url = "https://{IP}".format(IP=ip)
        elif port == 80:
            url = "http://{IP}".format(IP=ip)
        elif port == 8443:
            url = "https://{IP}:{PORT}".format(IP=ip, PORT=port)
        else:
            url = "http://{IP}:{PORT}".format(IP=ip, PORT=port)
        return url

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should this module be executed for this given service and port
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(GenericWebServiceModule, self).should_execute(service, port):
            return False
        # If any of the strings are in the service name
        if any(svc in service for svc in ["http", "http-proxy", "ssl", "https"]):
            return True
        # if any of the ports are the same as the port
        if any(prt == port for prt in [80, 443, 8080, 8008, 8443]):
            return True
        return False
