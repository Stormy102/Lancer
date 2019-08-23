#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules import nmap

__license__ = "GPL-3.0"

import config
import lancerargs
import utils

import sys
import signal
import os
import time


def main():
    # Register the signal handler for a more graceful Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Parse the arguments
    lancerargs.parse_arguments(sys.argv[1:])

    # Load the config file
    config.load_config()

    # Update the Windows virtual terminal if necessary
    utils.update_windows_virtual_terminal()

    # Display the splash screen
    show_header = config.config['Main']['Show Header']
    if show_header != 'no':
        utils.print_header()
    utils.version()

    # Language warning - not yet implemented
    if config.args.language_code != 'en':
        print(utils.error_message(), "Multi-language support is not yet implemented...")

    # Run the setup to make sure necessary files and permissions exist
    setup()

    if config.args.skipDisclaimer is not True:
        # Display the Legal disclaimer
        legal_disclaimer()

    # Get start time
    start_time = time.monotonic()
    # Run the program
    execute()

    print(utils.normal_message(), "Lancer has finished system scanning")
    elapsed_time = time.monotonic() - start_time

    print(utils.normal_message(), "Lancer took", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), "to complete")

    sys.exit(0)


def signal_handler(signal, frame):
    """
        Handles signal interrupts more gracefully than default behaviour
    """
    print("\n" + utils.error_message(), "Ctrl+C detected, terminating...")
    sys.exit(1)


def setup():
    """
    TODO: Use parameters/settings file for optional overriding
    :return: None
    """
    if not os.path.exists(config.nmap_cache()):
        os.makedirs(config.nmap_cache())
    if not os.path.exists(config.gobuster_cache()):
        os.makedirs(config.gobuster_cache())
    if not os.path.exists(config.ftp_cache()):
        os.makedirs(config.ftp_cache())

    if utils.is_user_admin() is False:
        print(utils.warning_message(), "Lancer doesn't appear to being run with elevated permissions."
                                       " Some functionality may not work correctly\n")


def legal_disclaimer():
    print(utils.error_message(), "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
                                 " authorisation is illegal.\n    It is the end user's responsibility to adhere to all"
                                 " local and international laws.\n    The developer(s) of this tool assume no liability"
                                 " and are not responsible for any misuse or damage caused by the use of this program")
    agree = utils.input_message("Press [Y] to agree:")
    if agree.lower() != "y":
        print(utils.error_message(), "Legal disclaimer has not been accepted. Exiting...")
        sys.exit(0)
    print("")


def execute():
    # If we have passed an nmap xml file
    if config.args.nmapFile is not None:
        print(utils.normal_message(), "Loading nmap file")
        utils.parse_nmap_scan(config.args.nmapFile)
    else:
        if config.args.quiet:
            nmap.nmap_scan(True)
        else:
            nmap.nmap_scan(False)


if __name__ == "__main__":
    # try:
    main()
    # except SystemExit:
    #    print(NormalMessage(), "Lancer is shutting down")
    # except:
    #    print(ErrorMessage(), "An unexpected error has occurred")
