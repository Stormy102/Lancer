#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from core.CriticalProgramNotInstalled import CriticalProgramNotInstalled
from core import utils
from modules.BaseModule import BaseModule
from modules.ModuleExecuteState import ModuleExecuteState
from modules.Nmap import Nmap

# To ensure that a module is correctly imported, ensure
# that an import declaration is inserted here
# noinspection PyUnresolvedReferences
from modules.FTPAnonymousAccess import FTPAnonymousAccess
# noinspection PyUnresolvedReferences
from modules.FTPBanner import FTPBanner
# noinspection PyUnresolvedReferences
from modules.GeolocateIP import GeolocateIP
# noinspection PyUnresolvedReferences
from modules.Gobuster import Gobuster
# noinspection PyUnresolvedReferences
from modules.Nikto import Nikto
# noinspection PyUnresolvedReferences
from modules.SSLCertificateExtractor import SSLCertificateExtractor


def main():
    try:
        initialise_provider()
        execute_modules()
    except CriticalProgramNotInstalled as err:
        print(err)


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
            # module.execute("127.0.0.1", 0)
            print(utils.normal_message(), "Executing", module.name)
        elif run_state is ModuleExecuteState.CannotExecute:
            raise CriticalProgramNotInstalled("{PROGRAM} is not installed".format(PROGRAM=module.name))
        else:
            print(utils.warning_message(), module.name, "is not installed, skipping...")


def get_modules() -> list:
    return BaseModule.__subclasses__()

