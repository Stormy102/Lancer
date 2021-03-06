# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule


class SMBClient(BaseModule):

    def __init__(self):
        super(SMBClient, self).__init__(name="SMB Client",
                                        description="Enumerates SMB shares",
                                        loot_name="smb",
                                        multithreaded=False,
                                        intrusive=True,
                                        critical=False)
        self.required_programs = ["smbclient"]

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the SMB Client module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(SMBClient, self).should_execute(service, port):
            return False
        if port == 445:
            return True
        if "microsoft-ds" in service:
            return True
        return False
