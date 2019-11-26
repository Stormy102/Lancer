#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

__license__ = "GPL-3.0"

from core import ArgHandler, config, winutils, utils
from modules.legacy import nmap
from core.Target import Target

import sys
import signal
import os
import time
import platform


def main():
    if config.args.skipDisclaimer is not True:
        # Display the Legal disclaimer
        legal_disclaimer()

    # Get start time
    start_time = time.monotonic()

    # Detect if we have a target list or just a single target
    if config.args.target is None:
        # Target list
        targets = config.args.host_file.read().splitlines()

        for target in targets:
            if len(target.strip()) == 0:
                continue
            # Comments start with a hashtag
            if len(target.strip()) > 0 and target[0] == "#":
                continue

            try:
                target = Target(target)
                execute(target)
                target.stop_timer()
            except ValueError as err:
                print(utils.error_message(), err)
            print()

    else:
        try:
            target = Target(config.args.target)
            execute(target)
            target.stop_timer()
        except ValueError as err:
            print(utils.error_message(), err)

    print(utils.normal_message(), "Lancer has finished system scanning")
    elapsed_time = time.monotonic() - start_time

    print(utils.normal_message(), "Lancer took {TIME} to complete".
          format(TIME=time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

    sys.exit(0)


def init():
    # Register the signal handler for a more graceful Ctrl+C
    signal.signal(signal.SIGINT, utils.signal_handler)

    # Load the config file
    config.load_config()

    # Parse the arguments
    ArgHandler.parse_arguments(sys.argv[1:])

    # Check we're on a supported Python version
    utils.python_version()

    # Update the Windows virtual terminal if necessary
    # If we're on Windows 10, import winutils
    if platform.system().lower() == "windows" and platform.release() == "10":
        winutils.update_windows_virtual_terminal()

    # Language warning - not yet implemented
    if config.args.language_code != 'en':
        print(utils.error_message(), "Multi-language support is not yet implemented...")

    # Run the setup to make sure necessary files and permissions exist
    setup()


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
    if not os.path.exists(config.nikto_cache()):
        os.makedirs(config.nikto_cache())

    if utils.is_user_admin() is False:
        print(utils.warning_message(), "Lancer doesn't appear to being run with elevated permissions\n"
                                       "    Some functionality may not work correctly\n")


def legal_disclaimer():
    print(utils.error_message(), "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
                                   " authorisation is illegal.\n    It is the end user's responsibility to adhere to "
                                   "all local and international laws.\n    The developer(s) of this tool assume no "
                                   "liability and are not responsible for any misuse or damage\n    caused by the use"
                                   "of this program")
    agree = utils.input_message("Press [Y] to agree:")
    if agree.lower() != "y":
        print(utils.error_message(), "Legal disclaimer has not been accepted. Exiting...")
        sys.exit(1)
    print("")


def execute(target: Target):
    config.current_target = target.ip
    # If we have passed an nmap xml file
    if config.args.nmapFile is not None:
        print(utils.normal_message(), "Loading nmap file")
        nmap.parse_nmap_scan(config.args.nmapFile)
    else:
        if config.args.quiet:
            nmap.nmap_scan(True)
        else:
            nmap.nmap_scan(False)


if __name__ == "__main__":
    """`Lancer` entry point"""
    init()
    main()
