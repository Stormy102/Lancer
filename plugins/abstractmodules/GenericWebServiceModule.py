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
    def __init__(self, name: str, description: str, loot_name: str, multithreaded: bool, intrusive: bool,
                 critical: bool):
        super(GenericWebServiceModule, self).__init__(name=name,
                                                      description=description,
                                                      loot_name=loot_name,
                                                      multithreaded=multithreaded,
                                                      intrusive=intrusive,
                                                      critical=critical)

    # noinspection PyMethodMayBeStatic
    def get_url(self, ip, port) -> str:
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
        # Check if this module is disabled in the config.ini file
        if not super(GenericWebServiceModule, self).should_execute(service, port):
            return False
        if service == "http":
            return True
        if "ssl" in service:
            return True
        if "https" in service:
            return True
        if service == "http-proxy":
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
