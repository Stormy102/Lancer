# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from core.CriticalProgramNotInstalled import CriticalProgramNotInstalled
from core import utils, config
from core.BaseModule import BaseModule
from core.ModuleExecuteState import ModuleExecuteState
from modules.Nmap import Nmap

# To ensure that a module is correctly imported, ensure
# that an import declaration is inserted here
# noinspection PyUnresolvedReferences
# from modules.FTPAnonymousAccess import FTPAnonymousAccess
# noinspection PyUnresolvedReferences
# from modules.FTPBanner import FTPBanner
# noinspection PyUnresolvedReferences
# from modules.GeolocateIP import GeolocateIP
# noinspection PyUnresolvedReferences
# from modules.Gobuster import Gobuster
# noinspection PyUnresolvedReferences
# from modules.Nikto import Nikto
# noinspection PyUnresolvedReferences
# from modules.SSLCertificateExtractor import SSLCertificateExtractor
# noinspection PyUnresolvedReferences
# from modules.SMBClient import SMBClient
# noinspection PyUnresolvedReferences
# from modules.Searchsploit import Searchsploit
# noinspection PyUnresolvedReferences
# from modules.HTTPHeaders import HTTPHeaders
# noinspection PyUnresolvedReferences
# from modules.GetHostname import GetHostname
# noinspection PyUnresolvedReferences
# from modules.HTTPOptions import HTTPOptions
# noinspection PyUnresolvedReferences
# from modules.GetWebsiteLinks import GetWebsiteLinks

import sys
import importlib.util
import os

LOADED_MODULES = []


def load_modules():
    for file in os.listdir("modules"):
        if not os.path.isfile("modules/" + file):
            continue
        if not file[-3:] == ".py":
            continue
        if file.endswith("__init__.py"):
            continue
        print("Importing " + file)
        module = importlib.import_module("modules.{CLASS}".format(CLASS=file[0:-3]))
        instance = getattr(module, file[0:-3])()
        print("Successfully imported {MODULE} ({MODULE_DESC})"
              .format(MODULE=instance.name, MODULE_DESC=instance.description))
        LOADED_MODULES.append(instance)
    print("Successfully imported {COUNT} modules".format(COUNT=len(LOADED_MODULES)))


def check_module_dependencies():
    logger = config.get_logger("Module Provider")
    # Iterate through every single subclass of BaseModule
    for subclass in get_modules():
        # Create an instance of the module
        module = subclass()
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
    try:
        load_modules()
        initialise_provider()
        execute_modules()
    except CriticalProgramNotInstalled as err:
        print(utils.warning_message(), err)


def initialise_provider():

    nmap = Nmap()

    if nmap.can_execute_module() is ModuleExecuteState.CanExecute:
        nmap.execute("127.0.0.1")
    else:
        raise CriticalProgramNotInstalled("Nmap is not installed")


def execute_modules():
    # Iterate through every single subclass of BaseModule
    for subclass in get_modules():
        # Create an instance of the module
        module = subclass()
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


def get_modules() -> list:
    return BaseModule.__subclasses__()

