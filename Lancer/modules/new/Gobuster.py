#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.new.BaseModule import BaseModule

import subprocess
import io
import Loot
import time
import utils


class Gobuster(BaseModule):
    def __init__(self):
        super(Gobuster, self).__init__(name="Gobuster",
                                       description="Enumerate a web server's directories to find hidden files",
                                       loot_name="Gobuster",
                                       multithreaded=False,
                                       intrusive=True,
                                       critical=False)
        self.required_programs = ["gobuster"]

    def execute(self, ip: str, port: int) -> None:
        self.create_loot_space(ip, port)
        Loot.loot[ip][str(port)][self.loot_name] = []

        out_file = "gobuster-{URL}-{PORT}".format(URL=ip, PORT=port)

        if port is 443:
            url = "https://{IP}".format(IP=ip)
        else:
            url = "http://{IP}:{PORT}".format(IP=ip, PORT=port)

        filename = "output.log"
        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            command = "gobuster dir -z -q -u {URL} -w {WORDLIST}" \
                .format(URL=url,
                        WORDLIST="C:\\Users\\Matthew\\Downloads\\Gobuster\\small.txt",)
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
                    result = {"Path": response_dir, "Code": code, "Code Value": human_readable_code}
                    Loot.loot[ip][str(port)][self.loot_name].append(result)

    def should_execute(self, service: str, port: int) -> bool:
        if service is "http":
            return True
        if service is "ssl/https":
            return True
        if port is 80:
            return True
        if port is 8080:
            return True
        if port is 8008:
            return True
        return False
