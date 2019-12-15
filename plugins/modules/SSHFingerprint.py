# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.SSHModule import SSHModule
from core.config import get_module_cache
from core.utils import normal_message
from core import Loot
from sshpubkeys import SSHKey, InvalidKeyError

import os
import subprocess
import io
import time


class SSHFingerprint(SSHModule):

    def __init__(self):
        super(SSHFingerprint, self).__init__(name="SSH Fingerprint",
                                             description="Get the SSH server's public key fingerprint",
                                             loot_name="ssh-fingerprint",
                                             intrusion_level=2)
        self.required_programs = ["ssh-keyscan"]

    def execute(self, ip: str, port: int) -> None:
        """
        Get the key type, bits and MD5 fingerprint of the SSH server
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)
        Loot.loot[ip][str(port)][self.loot_name] = []

        filename = os.path.join(get_module_cache(self.name, ip, str(port)), "ssh-fingerprint.log")

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -p - port to use
            command = ["ssh-keyscan", "-p", str(port), ip]
            process = subprocess.Popen(command, stdout=writer, stderr=writer)
            # While the process return code is None
            output = ""
            while process.poll() is None:
                output += reader.read().decode("UTF-8")
                time.sleep(0.5)
            output = reader.read().decode("UTF-8")
            output = output.splitlines()
            for line in output:
                if "#" in line:
                    continue
                # Get the key - this is after the first space as
                # ssh-keyscan returns IP KEY-TYPE KEY COMMENTS
                # 192.168.0.4 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEGODBKRjsFB/1v3pDRGpA6xR+QpOJg9vat0brlbUNDD root@Svr
                key_line = line[line.index(" ")+1:]
                key = SSHKey(key_line)
                try:
                    key.parse()
                    type = key_line[4:key_line.index(" ")]
                    key_hash = key.hash_md5()[4:]
                    results = {
                        "SSH Key Fingerprint": key_hash,
                        "Key Type": type,
                        "Bits": key.bits
                    }
                    Loot.loot[ip][str(port)][self.loot_name].append(results)
                    self.logger.log("Found {TYPE} key, {BITS} bits with fingerprint {FINGERPRINT}"
                                    .format(TYPE=type, BITS=key.bits, FINGERPRINT=key_hash))
                except InvalidKeyError:
                    self.logger.error("Unable parse key - the host could be down or a malformed output from ssh-keyscan"
                                      " could have been returned.")
                except NotImplementedError:
                    self.logger.error("This key is not supported by the Python SSH Pub Keys package. Please create an"
                                      " issue on Lancer's Github page.")
