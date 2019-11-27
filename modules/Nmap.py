# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from modules.ModuleExecuteState import ModuleExecuteState
from shutil import which
from core import config, utils

import subprocess
import os


class Nmap(object):

    def __init__(self):
        self.name = "Nmap"
        self.description = "Scans the specified hostname/IP for open ports"
        self.loot_name = "nmap"
        self.multithreaded = False,
        self.intrusive = True,
        self.critical = True

    def execute(self, ip: str) -> None:
        # out_file = os.path.join(config.nmap_cache(), "nmap-{TARGET}.xml".format(TARGET=ip))

        """nmap_args = ['nmap', '-sC', '-sV', '-oX', out_file, config.current_target]

        if config.args.scan_udp:
            print(utils.normal_message(), "Scanning UDP ports, this may take a long time")
            nmap_args.append('-sU')

        print(utils.normal_message(), "Scanning open ports on", config.current_target + "...", end=' ')

        # with Spinner():
        output = subprocess.check_output(nmap_args).decode('UTF-8')"""

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
