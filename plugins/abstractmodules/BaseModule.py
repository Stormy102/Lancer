# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.ModuleExecuteState import ModuleExecuteState
from shutil import which
from core import Loot
from core.config import get_logger, module_enabled

import logging


class BaseModule(object):

    def __init__(self, name: str, description: str, loot_name: str, multithreaded: bool, intrusive: bool,
                 critical: bool, intrusion_level:int = 3, priority: int = 1):
        self.name = name
        self.description = description
        self.loot_name = loot_name

        self.required_programs = []

        self.multithreaded = multithreaded
        self.intrusive = intrusive
        self.intrusion_level = intrusion_level # TODO: Intrusion level for all modules instead of bool
        self.priority = priority  # TODO: Execute priority - some modules should execute after others have ran
        self.critical_module = critical

        self.logger = get_logger(name)

        self.logger.debug("Created {NAME} module instance".format(NAME=name))

        # Suppress the DEBUG output from the urllib3.connectionpool
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def execute(self, ip: str, port: int) -> None:
        """
        Execute the module
        :param ip: IP to use
        :param port: Port to use
        """
        # Add to central repository of loot
        # TODO: Test all modules write their output
        pass

    def create_loot_space(self, ip: str, port: int) -> None:
        """
        Create a loot space in the dictionary
        :param ip: The IP to use
        :param port:  The port to use
        """
        # TODO: Move generation of loot spaces to Loot::create_loot_space() -> dict
        str_port = str(port)
        if ip not in Loot.loot:
            Loot.loot[ip] = {}
        if str_port not in Loot.loot[ip]:
            Loot.loot[ip][str_port] = {}
        if self.loot_name not in Loot.loot[ip][str_port]:
            Loot.loot[ip][str_port][self.loot_name] = {}
        self.logger.debug("Created {NAME} loot space at [{IP}][{PORT}][{LOOT}]"
                          .format(NAME=self.name, IP=ip, PORT=port, LOOT=self.loot_name))

    def should_execute(self, service: str, port: int) -> bool:
        """
        Should this module be executed for this given service and port
        :param service: The service to check
        :param port: The port to check
        :return: Boolean if this module should be executed
        """
        # Check if this module is disabled in the config.ini file
        return module_enabled(self.name)

    def can_execute_module(self) -> ModuleExecuteState:
        """
        Checks if the current module can be executed
        :return: ModuleExecuteState
        """
        # Loop through every program required
        for program in self.required_programs:

            # Using which to determine if it is installed by calling it via command line
            if which(program.lower()) is None:
                # If this is a critical module, we need to ensure that we halt here
                if self.critical_module:
                    self.logger.error("Critical program {PROGRAM} not installed, halting...".
                                      format(PROGRAM=program, MODULE=self.name))
                    return ModuleExecuteState.CannotExecute
                # This isn't a critical value, so skip execution
                else:
                    # self.logger.warning("{PROGRAM} not installed".format(PROGRAM=program, MODULE=self.name))
                    return ModuleExecuteState.SkipExecute

        # We have found all of the required programs, so we can execute this module
        return ModuleExecuteState.CanExecute
