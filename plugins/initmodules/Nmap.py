# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.BaseModule import BaseModule
from core.ModuleExecuteState import ModuleExecuteState
from core.config import get_module_cache
from shutil import which

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

        self.logger.debug("Writing XML output to {PATH}.xml|.nmap|.gnmap".format(PATH=output_filename))

        # TODO: UDP scan - different Nmap entry point module that executes?

        self.logger.info("Starting Nmap scan of {TARGET}".format(TARGET=ip))
        # with Spinner():
        with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
            # Arguments:
            # -v  - Verbose output
            # -oA - Output in all formats
            command = "nmap -v -oA {OUTPUT_FILE} {TARGET}".format(TARGET=ip, OUTPUT_FILE=output_filename)
            process = subprocess.Popen(command, stdout=writer)
            # While the process return code is None
            while process.poll() is None:
                time.sleep(0.5)
            # output = reader.read().decode("UTF-8").splitlines()
        print()
        self.logger.info("Finished Nmap scan of {TARGET}".format(TARGET=ip))
        print()

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
