# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.CriticalProgramNotInstalled import CriticalProgramNotInstalled
from core import utils, config
from core.ModuleExecuteState import ModuleExecuteState

import sys
import importlib.util
import os
import operator


LOADED_INIT_MODULES = []
LOADED_MODULES = []

logger = None


def load():
    global logger
    logger = config.get_logger("Module Provider")
    # __load_abstract_modules()
    __load_init_modules()
    __load_modules()
    __check_module_dependencies()


def __load_init_modules():
    global logger
    path = "plugins/initmodules"
    for file in os.listdir(path):
        if not os.path.isfile(os.path.join(path, file)):
            continue
        if not file[-3:] == ".py":
            continue
        if file.endswith("__init__.py"):
            continue
        logger.debug("Importing {FILE}".format(FILE=file))
        module = importlib.import_module("plugins.initmodules.{CLASS}".format(CLASS=file[0:-3]))
        instance = getattr(module, file[0:-3])()

        logger.info("Successfully imported {MODULE} ({MODULE_DESC})"
                    .format(MODULE=instance.name, MODULE_DESC=instance.description))
        LOADED_INIT_MODULES.append(instance)
    print(utils.normal_message(), "Successfully imported {COUNT} init modules".format(COUNT=len(LOADED_INIT_MODULES)))


def __load_modules():
    path = "plugins/modules"
    for file in os.listdir(path):
        if not os.path.isfile(os.path.join(path, file)):
            continue
        if not file[-3:] == ".py":
            continue
        if file.endswith("__init__.py"):
            continue
        logger.debug("Importing {FILE}".format(FILE=file))
        module = importlib.import_module("plugins.modules.{CLASS}".format(CLASS=file[0:-3]))
        instance = getattr(module, file[0:-3])()

        logger.info("Successfully imported {MODULE} ({MODULE_DESC})"
                    .format(MODULE=instance.name, MODULE_DESC=instance.description))
        LOADED_MODULES.append(instance)
    print(utils.normal_message(), "Successfully imported {COUNT} modules".format(COUNT=len(LOADED_MODULES)))


def __check_module_dependencies():
    global logger
    # Iterate through every single subclass of BaseModule
    for module in LOADED_MODULES:
        # Check if we can run it
        run_state = module.can_execute_module()
        if run_state is ModuleExecuteState.CannotExecute:
            logger.error("Required {PROGRAM} is not installed, quitting...".format(PROGRAM=module.name))
            sys.exit(1)
        elif run_state is ModuleExecuteState.SkipExecute:
            logger.warning("{PROGRAM} is not installed, this module will be disabled".format(PROGRAM=module.name))
    print()


def main():
    global logger
    logger = config.get_logger("Module Provider")
    try:
        load()

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
