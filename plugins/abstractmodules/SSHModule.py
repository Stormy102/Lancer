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


class SSHModule(BaseModule):
    def __init__(self, name: str, description: str, loot_name: str, intrusion_level: int, critical: bool = False):
        super(SSHModule, self).__init__(name=name,
                                        description=description,
                                        loot_name=loot_name,
                                        intrusion_level=intrusion_level,
                                        critical=critical)

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should this module be executed for this given service and port
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(SSHModule, self).should_execute(service, port):
            return False
        if service == "ssh":
            return True
        if port == 22:
            return True
        return False
