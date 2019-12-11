# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core.config import get_module_cache
from core import Loot

import io
import time
import subprocess
import os


class SMBListShares(BaseModule):

    def __init__(self):
        super(SMBListShares, self).__init__(name="SMB List Shares",
                                            description="Gets a list of the publicly available shares",
                                            loot_name="smb-share-list",
                                            intrusion_level=3)
        # self.required_programs = ["smbclient"]

    def execute(self, ip: str, port: int) -> None:
        """
        Try and get a list of the publicly available shares
        :param ip: The IP to use
        :param port: The port to use
        """
        self.create_loot_space(ip, port)
        # List of dictionary results
        Loot.loot[ip][str(port)][self.loot_name] = []

        filename = os.path.join(get_module_cache(self.name, ip, str(port)), "smbclient-share-list.log")

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -U - the username to use. Using '' denotes a Null Session
            # -N - no password
            # -L - get a list of shares
            # -g - Output in a greppable format
            command = ["smbclient", "-U", "''", "-N", "-g", "-L", ip]
            process = subprocess.Popen(command, stdout=writer)
            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            output = reader.read().decode("UTF-8").splitlines()

            if "NT_STATUS_ACCESS_DENIED" not in output:
                # self.logger.log("Able to get share list")
                lines = output.splitlines()
                for line in lines:
                    if "|" in line:
                        split = line.split("|")
                        share_type = split[0]
                        share_name = split[1]
                        share_desc = split[2]
                        data = {
                            "Name": share_name,
                            "Description": share_desc,
                            "Type": share_type
                        }
                        print(data)
                        Loot.loot[ip][str(port)][self.loot_name].append(data)
                # self.logger.log("Discovered {LEN} shares".format(LEN=len(Loot.loot[ip][str(port)][self.loot_name])))
            else:
                self.logger.log("Unable to get share list - NT_STATUS_ACCESS_DENIED")

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the SMB Client module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(SMBListShares, self).should_execute(service, port):
            return False
        if port == 445:
            return True
        if "microsoft-ds" in service:
            return True
        return False
