# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.BaseModule import BaseModule
from core import utils, Loot, config

import subprocess
import io
import time
import os


class Gobuster(BaseModule):
    def __init__(self):
        super(Gobuster, self).__init__(name="Gobuster",
                                       description="Enumerate a web server's directories to find hidden files",
                                       loot_name="directory/file enumeration",
                                       multithreaded=False,
                                       intrusive=True,
                                       critical=False)
        self.required_programs = ["gobuster"]

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)
        # List of dictionary results
        Loot.loot[ip][str(port)][self.loot_name] = []

        if port is 443:
            url = "https://{IP}".format(IP=ip)
        elif port is 80:
            url = "http://{IP}".format(IP=ip)
        else:
            url = "http://{IP}:{PORT}".format(IP=ip, PORT=port)

        filename = os.path.join(config.get_module_cache(self.name, ip), "gobuster-{PORT}.log".format(PORT=port))

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -e - expanded URL (whole path is shown)
            # -z - Don't display the progress (X/Y Z%)
            # -q - Don't print the banner for Gobuster
            # -k - Skip SSL Cert verification
            # -x - File extension(s) to scan for. By default we just scan for .php
            #                                     TODO: Add ability to select extensions
            # -u - URL
            # -w - Wordlist
            command = "gobuster dir -z -q -e -k -u {URL} -w {WORDLIST} -x {EXTENSIONS}" \
                .format(URL=url,
                        WORDLIST="C:\\Users\\Matthew\\Downloads\\Gobuster\\small.txt",
                        EXTENSIONS=".php")
            process = subprocess.Popen(command, stdout=writer)

            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            responses = reader.read().decode("ascii").splitlines()
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

    def should_execute(self, service: str, port: int) -> bool:
        if service == "http":
            return True
        if service == "ssl/https":
            return True
        if service == "http-proxy":
            return True
        if service == "https-alt":
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
