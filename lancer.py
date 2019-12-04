#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

__license__ = "GPL-3.0"

from core import ArgHandler, config, utils, ModuleProvider, Loot
from core.reports.JSONReport import JSONReport
from core.reports.TerminalReport import TerminalReport
from core.Target import Target
from pathlib import Path
from core.ExitCode import ExitCode

import sys
import signal
import time
import platform
import ipaddress
import socket
import traceback
import os
import shutil

logger = None


def init():
    """
        Initialise all of the needed prerequisites for Lancer. This should:

        - Register the signal handler for Ctrl+C
        - Load the config file
        - Parse command line arguments
        - Show the header
        - Check that we're on a supported Python version
        - Show an option to update the VirtualTerminal registry key if on Win 10
        - Show a warning that localisation support is not yet implemented if there is a non-default -l parameter
        - Display a legal disclaimer about using Lancer for illegal use
        - Warn if the cache is over 500mb in size
        - Clear the cache if we want to
    """
    # Register the signal handler for a more graceful Ctrl+C
    signal.signal(signal.SIGINT, utils.signal_handler)

    # Load the config file
    config.load_config()

    # Parse the arguments
    ArgHandler.parse_arguments(sys.argv[1:])

    # Display the header
    utils.display_header()
    time.sleep(1.25)

    # Check we're on a supported Python version
    utils.python_version()

    # Update the Windows virtual terminal if necessary
    # If we're on Windows 10, import winutils
    if platform.system().lower() == "windows" and platform.release() == "10":
        from core.winutils import update_windows_virtual_terminal
        update_windows_virtual_terminal()

    # Language warning - not yet implemented
    if ArgHandler.get_language_code() != 'en':
        print(utils.error_message(), "Multi-language support is not yet implemented...")

    # Show a legal disclaimer
    disclaimer = utils.terminal_width_string(
        "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
        " authorisation is illegal. It is the end user's responsibility to adhere to all local"
        " and international laws. The developers of this tool assume no liability and are not"
        " responsible for any misuse or damage caused by the use of this program."
    )
    print(utils.error_message(), disclaimer)
    print()

    # Cache warning
    # If it is more than 500, we display a warning
    root_directory = Path(config.get_cache_path())
    size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) / 1048576  # Bytes -> Mb
    if size >= 500:
        print(utils.warning_message(), "Cache is {SIZE}mb in size".format(SIZE="{:.1f}".format(size)))

    # Clear the cache
    if ArgHandler.get_clear_cache():
        files = os.listdir(config.get_cache_path())
        for filename in files:
            file_path = os.path.join(config.get_cache_path(), filename)

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path) and file_path != config.get_current_cache_path():
                shutil.rmtree(file_path)
        print(utils.normal_message(), "Removed {NUM} items from the cache".format(NUM=len(files)))

    # Check if we are admin, display a relevant message
    if utils.is_user_admin():
        print(utils.normal_message(), "Lancer running with elevated permissions")
    else:
        non_admin_warning = utils.terminal_width_string("Lancer doesn't appear to being run with elevated"
                                                        " permissions. Some functionality may not work"
                                                        " correctly")
        print(utils.warning_message(), non_admin_warning)

    # Display warning about your IP address
    ip_address = utils.terminal_width_string(
        "Your IP Address has been detected as {IP}. This can be changed with -a [IP]"
    )
    print(utils.normal_message(), ip_address.format(IP=get_ip()))
    print()

    # Preload all of the modules
    ModuleProvider.load()


def get_ip():
    # https://stackoverflow.com/a/28950776/4524180
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        ip = s.getsockname()[0]
    except socket.timeout:
        ip = '127.0.0.1'
    except socket.gaierror:
        ip = '127.0.0.1'
    except WindowsError:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def main():
    """
        Start Lancer
    """

    # Get start time
    start_time = time.monotonic()

    scan_targets()

    print(utils.normal_message(), "Lancer has finished system scanning")
    elapsed_time = time.monotonic() - start_time

    generate_reports()

    print(utils.normal_message(), "Lancer took {TIME} to complete".
          format(TIME=time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))


def scan_targets():
    # Detect if we have a target list or just a single target
    if ArgHandler.get_target_file() is not None:
        # Target list
        targets = ArgHandler.get_target_file().read().splitlines()

        for target in targets:
            if len(target.strip()) == 0:
                continue
            # Comments start with a hashtag
            if len(target.strip()) > 0 and target[0] == "#":
                continue

            scan_target(target)
    elif ArgHandler.get_nmap_file() is not None:
        print(utils.normal_message(), "Loading nmap file")
        raise NotImplementedError("Loading from an Nmap file with -TF is not yet implemented")
        # nmap.parse_nmap_scan(ArgHandler.get_nmap_file())
    else:
        scan_target(ArgHandler.get_target())


def scan_target(target: str):
    try:
        # See if the target is an IP network
        ip_network = ipaddress.ip_network(target, strict=False)
        if ip_network.version is 6:
            raise NotImplementedError("IPv6 addresses are not yet supported")
        for x in range(ip_network.num_addresses):
            ip = ip_network[x]
            tgt = Target(None, ip)
            ModuleProvider.analyse(tgt)
            tgt.stop_timer()
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
        tgt = Target(target, ip)
        ModuleProvider.analyse(tgt)
        tgt.stop_timer()
    print()


def generate_reports():
    logger.debug("Generating reports")
    report = JSONReport()
    report.generate_report(Loot.loot)
    report = TerminalReport()
    report.generate_report(Loot.loot)
    logger.debug("Finished generating reports")


if __name__ == "__main__":
    init()
    logger = config.get_logger("Main")
    try:
        main()
    except NotImplementedError as e:
        logger.error(e)
        sys.exit(ExitCode.NotImplemented)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print(utils.error_message(), "Unknown error encountered ({ERR}) - please report this via Github\n{EXCEPTION}"
              .format(ERR=e.args[0], EXCEPTION="".join(tb)))
        sys.exit(ExitCode.UnknownError)
    finally:
        print()
        print(utils.normal_message(), "Thank you for using Lancer")
        config.save_config()
