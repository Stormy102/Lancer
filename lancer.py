#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

__license__ = "GPL-3.0"

from core import ArgHandler, config, winutils, utils, ModuleProvider
from modules.legacy import nmap
from core.Target import Target
from pathlib import Path

import sys
import signal
import time
import platform
import ipaddress
import socket


def main():
    disclaimer = utils.terminal_width_string(
        "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
        " authorisation is illegal. It is the end user's responsibility to adhere to all local"
        " and international laws. The developer(s) of this tool assume no liability and are not"
        " responsible for any misuse or damage caused by the use of this program"
    )
    print(utils.error_message(), disclaimer)
    print()

    cache_size_check()

    admin_check()

    ModuleProvider.check_module_dependencies()

    # Get start time
    start_time = time.monotonic()

    scan_targets()

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


def admin_check():
    if utils.is_user_admin() is False:
        non_admin_warning = utils.terminal_width_string("Lancer doesn't appear to being run with elevated"
                                                        " permissions. Some functionality may not work"
                                                        " correctly")
        print(utils.warning_message(), non_admin_warning)
    else:
        print(utils.normal_message(), "Lancer running with elevated permissions")
    print()


def cache_size_check():
    root_directory = Path(config.get_cache_path())
    size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    kb = size / 1024
    mb = kb / 1024
    if mb >= 500:
        print(utils.warning_message(), "Cache is {SIZE}mb in size".format(SIZE="{:.1f}".format(mb)))
        print()


def scan_targets():
    # Detect if we have a target list or just a single target
    if config.args.host_file is not None:
        # Target list
        targets = config.args.host_file.read().splitlines()

        for target in targets:
            if len(target.strip()) == 0:
                continue
            # Comments start with a hashtag
            if len(target.strip()) > 0 and target[0] == "#":
                continue

            scan_target(target)
    elif config.args.nmapFile is not None:
        print(utils.normal_message(), "Loading nmap file")
        nmap.parse_nmap_scan(config.args.nmapFile)
    else:
        scan_target(config.args.target)


def scan_target(target: str):
    try:
        # See if the target is an IP network
        ip_network = ipaddress.ip_network(target, strict=False)
        if ip_network.version is 6:
            print(utils.error_message(), "IPv6 addresses are not yet supported\n")
            return
        for x in range(ip_network.num_addresses):
            ip = ip_network[x]
            target = Target("", ip)
            execute(target)
            target.stop_timer()
    except ValueError:
        # It's not an IP address or a subnet,
        # so most likely a hostname

        if target.startswith("www."):
            www_warning = utils.terminal_width_string(
                "Target starts with \"www.\" - this is not recommended as it can lead to false positives in modules "
                " - for example, when checking URLs for internal links. Do you want to remove \"www.\" from the URL?"

            )
            print(utils.warning_message(), www_warning)
            agree = utils.input_message("[Y]es or [N]o: ")
            if agree.lower() == "y":
                target = target.replace("www.", "")
                print(utils.normal_message(), "Removed \"www.\" from target, now \"{TARGET}\"".format(TARGET=target))
            else:
                print(utils.warning_message(), "Retaining \"www.\" in target")

        hostname_info = socket.getaddrinfo(target, None, socket.AF_INET)
        ip = ipaddress.ip_address(hostname_info[0][4][0])
        target = Target(target, ip)
        execute(target)
        target.stop_timer()
    print()


def execute(target: Target):
    # TODO: Use hostname if module allows it
    config.current_target = str(target.ip)
    nmap.nmap_scan()

if __name__ == "__main__":
    """`Lancer` entry point"""
    init()
    main()
