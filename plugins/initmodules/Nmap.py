# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.EventQueue import EventQueue
from plugins.abstractmodules.BaseModule import BaseModule
from core.ModuleExecuteState import ModuleExecuteState
from core.config import get_module_cache
from core import Loot
from shutil import which
from xml.dom import minidom
from cpe_utils import CPE

import os
import io
import subprocess
import time


class Nmap(BaseModule):

    def __init__(self):
        super(Nmap, self).__init__(name="Nmap",
                                   description="Scans the specified hostname/IP/IP subnet for open ports",
                                   loot_name="nmap",
                                   multithreaded=False,
                                   intrusive=False,
                                   critical=True)

    def execute(self, ip: str, port: int) -> None:
        # Don't specify filename on output_filename as all formats are specified
        output_filename = os.path.join(get_module_cache(self.name, ip, ""), "nmap")
        filename = os.path.join(get_module_cache(self.name, ip, ""), "nmap.log")

        self.logger.debug("Writing output to {PATH}.xml|.nmap|.gnmap".format(PATH=output_filename))

        # TODO: Optional UDP scan

        self.logger.info("Starting Nmap scan of {TARGET}".format(TARGET=ip))

        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -v  - Verbose output
            # -sT - TCP scan
            # -sV - Version detection
            # -oA - Output in all formats
            command = "nmap -v -sT -sV -oA {OUTPUT_FILE} {TARGET}".format(TARGET=ip, OUTPUT_FILE=output_filename)
            process = subprocess.Popen(command, stdout=writer)
            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            # output = reader.read().decode("UTF-8").splitlines()
        self.logger.info("Finished Nmap scan of {TARGET}".format(TARGET=ip))

        # Parse the XML output
        xml = minidom.parse("{FILE}.xml".format(FILE=output_filename))
        # Get the host scanned
        hostslist = xml.getElementsByTagName('hosts')
        # We only scan one host at a time
        if int(hostslist[0].attributes['down'].value) > 0:
            # Unreachable, return rest of the processing
            self.logger.warning("{TARGET} was unreachable".format(TARGET=ip))
            return

        # Get all of the open ports
        port_list = xml.getElementsByTagName('port')
        self.logger.info("{PORT_COUNT} ports are open".format(PORT_COUNT=len(port_list)))

        # Get all of the CPE versions detected
        cpe_list = list(dict.fromkeys([x.firstChild.nodeValue for x in xml.getElementsByTagName('cpe')]))
        for cpe in cpe_list:
            self.logger.info("Detected {CPE}".format(CPE=CPE(cpe).human()))

        # searchsploit_nmap_scan(out_file)

        # Loop through the open ports
        for open_port in port_list:
            # Get the service type
            for svc in open_port.getElementsByTagName('service'):
                # Parse the values
                service = svc.attributes['name'].value
                port = open_port.attributes['portid'].value

                # If the IP/port is not in the Loot dictionary, add it
                if ip not in Loot.loot:
                    Loot.loot[ip] = {}
                if port not in Loot.loot[ip]:
                    Loot.loot[ip][port] = {}

                # Add to the event Queue so we get a notification
                EventQueue.push(service=service, port=int(port))

    def can_execute_module(self) -> ModuleExecuteState:
        """
        Checks if the current module can be executed
        :return: ModuleExecuteState
        """
        # Using which to determine if it is installed by calling it via command line
        if which("nmap") is None:
            return ModuleExecuteState.CannotExecute

        # We have found all of the required programs, so we can execute this module
        return ModuleExecuteState.CanExecute
