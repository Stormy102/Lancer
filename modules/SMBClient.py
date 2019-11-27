# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule


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
        # TODO:
        # if not super(SMBClient, self).should_execute(service, port):
        #     return False
        if port == 445:
            return True
        if "microsoft-ds" in service:
            return True
        return False
