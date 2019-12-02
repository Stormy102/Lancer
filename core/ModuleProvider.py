# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.CriticalProgramNotInstalled import CriticalProgramNotInstalled
from core import utils, config
from core.ModuleExecuteState import ModuleExecuteState
from modules.Nmap import Nmap

import sys
import importlib.util
import os
import operator

LOADED_MODULES = []

logger = None


def load_modules():
    for file in os.listdir("modules"):
        if not os.path.isfile("modules/" + file):
            continue
        if not file[-3:] == ".py":
            continue
        if file.endswith("__init__.py"):
            continue
        logger.debug("Importing {FILE}".format(FILE=file))
        module = importlib.import_module("modules.{CLASS}".format(CLASS=file[0:-3]))
        instance = getattr(module, file[0:-3])()

        logger.info("Successfully imported {MODULE} ({MODULE_DESC})"
                    .format(MODULE=instance.name, MODULE_DESC=instance.description))
        LOADED_MODULES.append(instance)
    print(utils.normal_message(), "Successfully imported {COUNT} modules".format(COUNT=len(LOADED_MODULES)))
    print()


def check_module_dependencies():
    # Iterate through every single subclass of BaseModule
    for module in LOADED_MODULES:
        # Check if we can run it
        run_state = module.can_execute_module()
        if run_state is ModuleExecuteState.CannotExecute:
            logger.error("Required {PROGRAM} is not installed, quitting...".format(PROGRAM=module.name))
            sys.exit(1)
        elif run_state is ModuleExecuteState.SkipExecute:
            msg = "{PROGRAM} is not installed, this module will be temporarily disabled".format(PROGRAM=module.name)
            logger.warning(msg)
            print(utils.warning_message(), msg)
    print()


def main():
    global logger
    logger = config.get_logger("Module Provider")
    try:
        load_modules()
        check_module_dependencies()

        initialise_provider()
        execute_modules()
    except CriticalProgramNotInstalled as err:
        print(utils.warning_message(), err)


def initialise_provider():
    # TODO: Instead of having an Nmap script as a module, instead, have nmap
    #       be an EntryPointModule which will make it more extensible in the
    #       future, such as quiet Nmap and loud Nmap scans
    nmap = Nmap()

    if nmap.can_execute_module() is ModuleExecuteState.CanExecute:
        nmap.execute("127.0.0.1", 0)
    else:
        raise CriticalProgramNotInstalled("Nmap is not installed")


def execute_modules():
    global LOADED_MODULES
    # Order according to priority
    LOADED_MODULES = sorted(LOADED_MODULES, key=operator.attrgetter('priority'), reverse=True)
    # Iterate through every single instance of our modules
    for module in LOADED_MODULES:
        # Check if we can run it
        run_state = module.can_execute_module()
        if run_state is ModuleExecuteState.CanExecute:
            service = "service"
            ip = "127.0.0.1"
            port = 0

            if module.should_execute(service, port):
                print(utils.normal_message(), "Executing {PROGRAM}".format(PROGRAM=module.name))
                module.execute(ip, port)

        elif run_state is ModuleExecuteState.CannotExecute:
            raise CriticalProgramNotInstalled("{PROGRAM} is not installed".format(PROGRAM=module.name))
        else:
            print(utils.warning_message(), "{PROGRAM} is not installed, skipping...".format(PROGRAM=module.name))
