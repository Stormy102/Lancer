#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from modules.new.BaseModule import BaseModule

import ftplib
import Loot


class FTPBanner(BaseModule):
    def __init__(self):
        super(FTPBanner, self).__init__(name="FTP Banner",
                                                 description="Gets the banner for the FTP server",
                                                 loot_name="FTP Banner",
                                                 multithreaded=False,
                                                 intrusive=True,
                                                 critical=False)

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)

        ftp_client = ftplib.FTP()
        ftp_client.connect(ip, port)
        # print(utils.warning_message(), "FTP Server banner:", ftp_client.getwelcome()[4:])
        Loot.loot[ip][str(port)][self.loot_name]["Banner"] = ftp_client.getwelcome()
        ftp_client.quit()

    def should_execute(self, service: str, port: int) -> bool:
        if service is "ftp":
            return True
        if port is 21:
            return True
        return False
