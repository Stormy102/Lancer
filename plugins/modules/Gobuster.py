# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import utils, Loot, config

import subprocess
import io
import time
import os


class Gobuster(GenericWebServiceModule):
    def __init__(self):
        super(Gobuster, self).__init__(name="Gobuster",
                                       description="Enumerate a web server's directories to find hidden files",
                                       loot_name="directory/file enumeration",
                                       intrusion_level=3)
        self.required_programs = ["gobuster"]

    def execute(self, ip: str, port: int) -> None:
        """
        Enumerates files and directories on the given web server
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)
        # List of dictionary results
        Loot.loot[ip][str(port)][self.loot_name] = []

        url = self.get_url(ip, port)

        filename = os.path.join(config.get_module_cache(self.name, ip), "enum-{PORT}.log".format(PORT=port))

        wordlist_path = config.get_module_value(self.name, "wordlist",
                                                "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")

        if not os.path.exists(wordlist_path):
            msg = utils.terminal_width_string(
                "Unable to find Gobuster wordlist at {PATH}".format(PATH=wordlist_path)
            )
            self.logger.error(msg)
            return

        extensions = config.get_module_value(self.name, "extensions", ".php,.txt")

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -e - expanded URL (whole path is shown)
            # -z - Don't display the progress (X/Y Z%)
            # -q - Don't print the banner for Gobuster
            # -k - Skip SSL Cert verification
            # -x - File extension(s) to scan for. Value loaded from config.ini with .php,.txt as default
            # -u - URL
            # -w - Wordlist
            command = "gobuster dir -z -q -e -k -u {URL} -w {WORDLIST} -x {EXTENSIONS}" \
                .format(URL=url, WORDLIST=wordlist_path, EXTENSIONS=extensions)
            process = subprocess.Popen(command, stdout=writer)

            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
                responses = reader.read().decode("UTF-8").splitlines()
                for response in responses:
                    if response.strip() is not "":
                        # Get the response code (last three chars but one)
                        code = int(response[-4:-1])
                        # Get this as a human readable response
                        human_readable_code = utils.get_http_code(code)
                        # Get the directory
                        response_dir = response.split('(')[0].strip()
                        # Add to the loot
                        result = {"Path": response_dir, "Code": code, "Code Value": human_readable_code}
                        Loot.loot[ip][str(port)][self.loot_name].append(result)
                        print(utils.warning_message(), "Found directory at {PATH} with {CODE} ({CODE_VALUE}"
                              .format(PATH=response_dir, CODE=code, CODE_VALUE=human_readable_code))
