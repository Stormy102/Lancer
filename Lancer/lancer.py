#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lancer modules
from modules.nmap import *
# Lancer utils
from utils import *

__license__ = "GPL-3.0"

import lancerargs
# Lancer config
import config
# Python modules
import sys
import signal


def main():
    # Register the signal handler for a more graceful Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check if we are on Windows 10 and if we have the VirtualTerminalLevel set to 1
    if is_not_virtual_terminal():
        print("\n[*] To enable output colouring in the console, we need to set a registry value"
              " (HKCU\\Console\\VirtualTerminalLevel). Do you wish to continue? [Y/N]")
        if input("> ").lower() == "y":
            set_virtual_terminal()

    # Parse the arguments
    lancerargs.parse_arguments(sys.argv[1:])
    
    # Display the splash screen
    print_header()
    version()
    
    # Run the setup to make sure necessary files and permissions exist
    setup()

    if config.args.skipDisclaimer is not True:
        # Display the Legal disclaimer
        legal_disclaimer()
    
    # Run the program
    execute()

    print(normal_message(), "Lancer has finished system scanning")
    
    sys.exit(0)


def signal_handler(signal, frame):
    """
        Handles signal interrupts more gracefully than default behaviour
    """
    print(error_message(), "Ctrl+C detected, terminating...")
    sys.exit(1)


def setup():
    """
    TODO: Use parameters/settings file for optional overriding
    :return: None
    """
    if not os.path.exists("nmap"):
        os.makedirs("nmap")
    if not os.path.exists("gobuster"):
        os.makedirs("gobuster")
    if not os.path.exists("ftp"):
        os.makedirs("ftp")

    if is_user_admin() is False:
        print(warning_message(), "Lancer doesn't appear to being run with elevated permissions."
                                 " Some functionality may not work correctly\n")


def legal_disclaimer():
    print(error_message(), "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
                           " authorisation is illegal.\n    It is the end user's responsibility to adhere to all"
                           " local and international laws.\n    The developer(s) of this tool assume no liability"
                           " and are not responsible for any misuse or damage caused by the use of this program")
    agree = input_message("Press [Y] to agree:")
    if agree.lower() != "y":
        print(error_message(), "Legal disclaimer has not been accepted. Exiting...")
        sys.exit(0)
    print("")


def execute():
    # If we have passed an nmap xml file
    if config.args.nmapFile is not None:
        print(normal_message(), "Loading nmap file")
        parse_nmap_scan(config.args.nmapFile)
    else:
        if config.args.quiet:
            nmap_scan(True)
        else:
            nmap_scan(False)

    
if __name__ == "__main__":
    # try:
    main()
    # except SystemExit:
    #    print(NormalMessage(), "Lancer is shutting down")
    # except:
    #    print(ErrorMessage(), "An unexpected error has occurred")
