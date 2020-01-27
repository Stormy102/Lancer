# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.SSHModule import SSHModule
from core.config import get_module_cache
from core import config, Loot
from string import ascii_letters
from random import choice

import os
import subprocess
import io
import time
import re


class SSHAuthMethods(SSHModule):

    def __init__(self):
        super(SSHAuthMethods, self).__init__(name="SSH Auth Methods",
                                             description="Get the auth methods that the SSH server supports",
                                             loot_name="ssh-auth-methods",
                                             intrusion_level=4)
        self.required_programs = ["ssh"]

    def execute(self, ip: str, port: int) -> None:
        """
        Test the authentication methods supported by the server
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)

        filename = os.path.join(get_module_cache(self.name, ip, str(port)), "ssh-auth-methods.log")

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            random_username = ''.join([choice(ascii_letters) for _ in range(0, 9)])
            # Arguments:
            # -p - port to use
            command = ["ssh", "-o", "ConnectTimeout={TIMEOUT}".format(TIMEOUT=config.get_timeout()),
                       "-o", "StrictHostKeyChecking=no", "-o", "PreferredAuthentications=none", "-o", "LogLevel=ERROR",
                       "-p", str(port), "{USER}@{IP}".format(USER=random_username, IP=ip)]
            process = subprocess.Popen(command, stdout=writer, stderr=writer)
            # While the process return code is None
            output = ""
            while process.poll() is None:
                output += reader.read().decode("UTF-8")
                time.sleep(0.5)
            output = reader.read().decode("UTF-8")
            auth_methods = re.search("\\((.*?)\\)", output)
            if auth_methods:
                auth_methods = auth_methods.group()
                # Trim the brackets from the text
                auth_methods = auth_methods[1:-1]
                # Split by comma
                auth_methods = auth_methods.split(",")
                self.logger.info("Supported auth methods are {METHODS}".format(METHODS=", ".join(auth_methods)))
                Loot.loot[ip][str(port)][self.loot_name] = auth_methods
            else:
                self.logger.error("Unable to get authentication types - maybe the host refused to connect")
