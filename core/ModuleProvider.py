# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.CriticalProgramNotInstalled import CriticalProgramNotInstalled
from core import utils, config
from core.ModuleExecuteState import ModuleExecuteState
from core.Target import Target
from core.ExitCode import ExitCode

import sys
import importlib.util
import os
import operator

LOADED_INIT_MODULES = []
LOADED_MODULES = []

logger = None

# TODO: Make a class


def load():
    global logger
    logger = config.get_logger("Module Provider")
    __check_plugin_folder()
    __load_init_modules()
    __load_modules()
    __check_module_dependencies()


def __check_plugin_folder() -> None:
    """
        Checks that the plugin folder exists. If not, it quits with the corresponding exit code
    """
    if not os.path.exists("plugins"):
        sys.exit(ExitCode.PluginDirectoryMissing)
    if not os.path.exists("plugins/initmodules"):
        sys.exit(ExitCode.EntryPointModulesNotLoaded)
    if not os.path.exists("plugins/modules"):
        sys.exit(ExitCode.ModuleDirectoryMissing)


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
            sys.exit(ExitCode.CriticalDependencyNotInstalled)
        elif run_state is ModuleExecuteState.SkipExecute:
            logger.warning("{PROGRAM} is not installed, this module will be disabled".format(PROGRAM=module.name))
    print()


def analyse(target: Target):
    global logger
    logger = config.get_logger("Module Provider")

    __execute_init_module(target)
    __execute_modules(target)


def __execute_init_module(target: Target):
    if len(LOADED_INIT_MODULES) > 0:
        module = LOADED_INIT_MODULES[0]

        if module.can_execute_module() is ModuleExecuteState.CanExecute:
            module.execute(target.get_address(), 0)
        else:
            print(utils.error_message(), "Unable to meet dependencies for {MODULE}. Quitting"
                  .format(MODULE=module.name))
            sys.exit(ExitCode.CriticalDependencyNotInstalled)
    else:
        print(utils.error_message(), "No Init Modules loaded. Quitting")
        sys.exit(ExitCode.EntryPointModulesNotLoaded)


def __execute_modules(target: Target):
    global LOADED_MODULES
    # Order according to priority
    LOADED_MODULES = sorted(LOADED_MODULES, key=operator.attrgetter('priority'), reverse=True)
    # Iterate through every single instance of our modules
    for module in LOADED_MODULES:
        # Check if we can run it
        run_state = module.can_execute_module()
        if run_state is ModuleExecuteState.CanExecute:
            service = "service"
            ip = str(target.ip)
            port = 0

            if module.should_execute(service, port):
                print(utils.normal_message(), "Executing {PROGRAM}".format(PROGRAM=module.name))
                module.execute(ip, port)

        elif run_state is ModuleExecuteState.CannotExecute:
            raise CriticalProgramNotInstalled("{PROGRAM} is not installed".format(PROGRAM=module.name))
