#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lancer modules
from modules.nmap import *
# Lancer utils
from utils import *

__license__ = "GPL-3.0"

# Lancer config
import config
# Python modules
import sys
import argparse
import signal
import time


def parse_arguments():

    example = 'Examples:\n\n'
    example += '$ python lancer.py -T 10.10.10.100 --verbose\n'
    example += '$ python lancer.py --target-file targets --skip-ports 445 8080 --show-program-output\n'
    example += '$ python lancer.py --target 192.168.1.10 --nmap nmap/bastion.xml /' \
               '\n  -wW /usr/share/wordlists/dirbuster/directory-2.3-small.txt /\n  -fD HTB -fU L4mpje -fP P@ssw0rd'
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Lancer - system vulnerability scanner\n\nThis tool is designed to"
                                                 " aid the recon phase of a pentest or any legal & authorised attack"
                                                 " against a device or network. The author does not take any liability"
                                                 " for use of this tool for illegal use.", epilog=example)

    main_args = parser.add_argument_group("Main arguments")
    mex_group = main_args.add_mutually_exclusive_group(required=True)
    mex_group.add_argument("-T", "--target", metavar="TARGET", dest='target', type=str, help="IP of target")
    mex_group.add_argument("--target-file", metavar="FILE", dest="hostfile", type=argparse.FileType('r'),
                           help="File containing a list of target IP addresses")
    main_args.add_argument("-q", "--quiet", dest='quiet', action="store_true", default='',
                           help="Do a quiet nmap scan. This will help reduce the footprint of the scan in logs and on"
                                " IDS which may be present in a network.")
    main_args.add_argument("-v", "--verbose", dest='verbose', action="store_true", default='',
                           help="Use a more verbose output. This will output more detailed information and may help to"
                                " diagnose any issues")
    main_args.add_argument("-sd", "--skip-disclaimer", dest='skipDisclaimer', action="store_true", default='',
                           help="Skip the legal disclaimer. By using this flag, you agree to use the program for legal"
                                " and authorised use")
    main_args.add_argument("--skip-ports", nargs='+', type=int, metavar="PORTS", dest='skipPorts', default=[],
                           help="Set the ports to ignore. These ports will have no enumeration taken against them,"
                                " except for the initial discovery via nmap. This can be used to run a custom scan and"
                                " pass the results to Lancer.")
    main_args.add_argument("--show-output", dest='show_output', action="store_true", default='',
                           help="Show the output of the programs which are executed, such as nmap, nikto, smbclient"
                                " and gobuster")
    main_args.add_argument("--nmap", metavar="FILE", dest='nmapFile', type=str,
                           help="Skip an internal nmap scan by providing the path to an nmap XML file")

    sgroup2 = parser.add_argument_group("Web Services", "Options for targeting web services")
    sgroup2.add_argument("-wW", metavar="WORDLIST", dest='webWordlist',
                         default='/usr/share/wordlists/dirbuster/directory-2.3-medium.txt',
                         help="The wordlist to use. Defaults to the directory-2.3-medium.txt file found in"
                              " /usr/share/wordlists/dirbuster")

    sgroup3 = parser.add_argument_group("File Services", "Options for targeting file services")
    sgroup3.add_argument("-fD", metavar="DOMAIN", dest='fileDomain',
                         help="Domain to use during the enumeration of file services")
    sgroup3.add_argument("-fU", metavar="USERNAME", dest='fileUsername',
                         help="Username to use during the enumeration of file services")
    sgroup3.add_argument("-fP", metavar="PASSWORD", dest='filePassword',
                         help="Password to use during the enumeration of file services")
    
    if len(sys.argv) is 1:
        print(error_message(), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)
    
    config.args = parser.parse_args()


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
    parse_arguments()
    
    # Display the splash screen
    splash_screen()
    
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
    if not os.path.exists("nmap"):
        os.makedirs("nmap")
    if not os.path.exists("gobuster"):
        os.makedirs("gobuster")

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
    #try:
    main()
    #except SystemExit:
        # Ignore
    #    print(NormalMessage(), "Lancer is shutting down")
    #except:
    #    print(ErrorMessage(), "An unexpected error has occured")
