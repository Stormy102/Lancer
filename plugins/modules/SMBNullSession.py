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


class SMBNullSession(BaseModule):

    def __init__(self):
        super(SMBNullSession, self).__init__(name="SMB Null Session",
                                             description="Checks if ",
                                             loot_name="smb-null-session",
                                             intrusion_level=3)
        self.required_programs = ["smbclient"]

    def execute(self, ip: str, port: int) -> None:
        """
        Check if the server supports a null SMB session
        :param ip: The IP to use
        :param port: The port to use
        """
        self.create_loot_space(ip, port)

        filename = os.path.join(get_module_cache(self.name, ip, str(port)), "smbclient-nullsession.log")

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -U - the username to use. Using '' denotes a Null Session
            # -N - no password
            # //{IP}/ipc$ - the path to the share to access
            # -c 'help - the command to execute upon connection
            command = ["smbclient", "-U", "''", "-N", "//{IP}/ipc$".format(IP=ip), "-c", "'help'"]
            process = subprocess.Popen(command, stdout=writer)
            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            output = reader.read().decode("UTF-8").splitlines()

            if "case_sensitive" in output:
                msg = "Successfully accessed {IP}/ipc$ using a Null Session".format(IP=ip)
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.warning(msg)
            elif "NT_STATUS_ACCESS_DENIED" in output:
                msg = "Permission denied trying to access {IP}/ipc$ - NT_STATUS_ACCESS_DENIED".format(IP=ip)
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.info(msg)
            elif "NT_STATUS_IO_TIMEOUT" in output:
                msg = "Connecting to {IP}/ipc$ timed out - NT_STATUS_IO_TIMEOUT".format(IP=ip)
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.info(msg)
            else:
                msg = "Unable to get a null session on {IP}/ipc$".format(IP=ip)
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.info(msg)

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should the SMB Client module be executed
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        if not super(SMBNullSession, self).should_execute(service, port):
            return False
        if port == 445:
            return True
        if "microsoft-ds" in service:
            return True
        return False
