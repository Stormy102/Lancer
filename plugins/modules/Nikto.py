# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core.config import get_module_cache
from core import utils
from xml.dom import minidom

import os
import io
import subprocess
import time


class Nikto(GenericWebServiceModule):
    def __init__(self):
        super(Nikto, self).__init__(name="Nikto",
                                    description="Scans the given web server",
                                    loot_name="nikto",
                                    intrusion_level=3)
        self.required_programs = ["nikto"]

    def execute(self, ip: str, port: int) -> None:
        """
        Scan the web server using Nikto
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)

        url = self.get_url(ip, port)
        output_filename = os.path.join(get_module_cache(self.name, ip, ""), "nmap")
        filename = os.path.join(get_module_cache(self.name, ip, ""), "nmap.log")

        self.logger.debug("Writing XML output to {PATH}.xml|.nmap|.gnmap".format(PATH=output_filename))

        self.logger.info("Starting Nmap scan of {TARGET}".format(TARGET=ip))
        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -host - the host to scan
            # -Format - the format of the output file
            # -o - the output path
            # -ask no - don't do anything which requires user input
            command = "nikto -host {URL} -Format xml -o {OUTPUT} -ask no"\
                .format(URL=url, OUTPUT=output_filename)
            process = subprocess.Popen(command, stdout=writer)
            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            # output = reader.read().decode("UTF-8").splitlines()

        xmldoc = minidom.parse(output_filename)
        nikto_items = xmldoc.getElementsByTagName('item')
        for item in nikto_items:
            print(utils.warning_message(), item.getElementsByTagName("description")[0].firstChild.wholeText)
