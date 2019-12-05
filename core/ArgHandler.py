# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.utils import normal_message, error_message, terminal_width_string
from core.config import __version__, get_config_path

import argparse
import io
import sys
import time

__args = argparse.Namespace()
__args.verbose = None
__args.very_verbose = None


def parse_arguments(args):
    global __args
    parser = create_parser()

    if len(args) is 0:
        print(error_message(), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)

    if len(args) is 1 and "--version" in args:
        print(normal_message(), "Lancer {VERSION}".format(VERSION=__version__))
        sys.exit(0)

    if len(args) is 1 and "-h" or "--help" in args:
        parser.print_help()
        sys.exit(0)

    __args = parser.parse_args(args)


def create_parser():
    example = 'Examples:\n'
    example += normal_message() + ' ./lancer -T 10.10.10.100 -v -l de -a 10.8.0.1\n'
    example += normal_message() + ' ./lancer -TF targets.lan -vv --cache-root ./cache/\n'
    example += terminal_width_string(
        normal_message() + ' ./lancer -TN nmap-10.0.0.1.xml --skip-ports 445 80 -L 5'
    )

    description = normal_message() + " Lancer - system vulnerability scanner\n"
    description += terminal_width_string(
        normal_message() + " See the config.ini file at {CONFIG_PATH} for more options."
        .format(CONFIG_PATH=get_config_path())
    )

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description, epilog=example, add_help=False)

    main_args = parser.add_argument_group("Required Arguments")
    main_args.description = "Specify the target or targets that Lancer will scan."
    mex_group = main_args.add_mutually_exclusive_group(required=True)
    mex_group.add_argument("-T", "--target", metavar="TARGET", dest='target', type=str,
                           help="The hostname, IPv4 address or a subnet of of IPv4 addresses you wish to analyse.")
    mex_group.add_argument("-TF", "--target-file", metavar="FILE", dest="host_file", type=argparse.FileType('r'),
                           help="File containing a list of target IP addresses.")
    mex_group.add_argument("-TN", "--target-nmap", metavar="FILE", dest='nmapFile', type=str,
                           help="Skip an internal Nmap scan by providing the path to an Nmap XML file. It is"
                                " recommended to run common scripts (-sC argument) and version detection (-sV"
                                " argument)")

    modules = parser.add_argument_group("Module Arguments (Coming soon)")
    modules.add_argument("--cache-root", metavar="PATH", dest='cache_root', default='',
                         help="[NOT YET IMPLEMENTED] "
                              "The root of the cache. This is where all of the data for the programs run is stored,"
                              " which may be useful if you wish to document or save all of the data in a separate"
                              " location.")
    modules.add_argument("-L", "--level", metavar="LEVEL", dest='intrusive_level', default=3,
                         help="[NOT YET IMPLEMENTED] "
                              "The intrusion level of this iteration. A level of 1 means the least intrusive scripts"
                              " will be run, such as Nmap on quiet mode and a few HTTP requests. A level of 5 will mean"
                              " that intrusive exploits will be run against the computer to determine how vulnerable it"
                              " is. A full list of modules and their intrusion levels can be found on the Github Wiki."
                              " This defaults to 3 - moderately intrusive.")
    modules.add_argument("-a", "--address", metavar="IP", dest='address', default='',
                         help="[NOT YET IMPLEMENTED] "
                              "Overrides the detected IP address with your own which is supplied.")
    modules.add_argument("--skip-ports", nargs='+', type=int, metavar="PORTS", dest='skipPorts', default=[],
                         help="Set the ports to ignore. These ports will have no enumeration taken against them,"
                              " except for the initial discovery via Nmap. This can be used to run a custom scan and"
                              " pass the results to Lancer. Best used in conjunction with -TN/--target-nmap.")

    output = parser.add_argument_group("Output Arguments")
    output.description = "Control the output of Lancer."
    verbose_group = output.add_mutually_exclusive_group(required=False)
    verbose_group.add_argument("-v", "--verbose", dest='verbose', action="store_true", default=False,
                               help="Use a verbose output. This will output results and information as modules run,"
                                    " which can be useful if you don't wish to wait for a report at the end.")
    verbose_group.add_argument("-vv", "--very-verbose", dest='very_verbose', action="store_true", default=False,
                               help="Use a very verbose output. This will output virtually every single event that"
                                    " Lancer logs. Useful for debugging.")
    output.add_argument("-o", "--output", metavar="FILE", dest="host_file", type=argparse.FileType('w'),
                        help="[NOT YET IMPLEMENTED] "
                             "Output the human-readable contents of the Lancer scan to a file. Best used in "
                             " conjunction with -v/-vv")
    output.add_argument("--version", dest='show_version', action="store_true", default='',
                        help="Shows the current version of Lancer.")

    optional_args = parser.add_argument_group("Optional Arguments")
    optional_args.add_argument("-l", "--language", metavar="LANGUAGE", dest="language_code", default="en", type=str,
                               help="[NOT YET IMPLEMENTED] "
                                    "Language you want Lancer to use in. The  language code uses ISO 639-1. Defaults to"
                                    " English.")

    optional_args.add_argument("-h", "--help", action="store_true", dest="help",
                               help="Shows the different arguments available for Lancer.")
    optional_args.add_argument("--clear-cache", action="store_true", dest="clear_cache",
                               help="Clear the cache before executing")

    return parser


def get_target() -> str:
    global __args
    if __args.target is None:
        return None
    return __args.target


def get_target_file() -> io.FileIO:
    global __args
    if __args.host_file is None:
        return None
    return __args.host_file


def get_nmap_file() -> io.FileIO:
    global __args
    if __args.nmapFile is None:
        return None
    return __args.nmapFile


def get_verbose() -> bool:
    global __args
    if __args.verbose is None:
        return False
    return __args.verbose


def get_very_verbose() -> bool:
    global __args
    if __args.very_verbose is None:
        return False
    return __args.very_verbose


def get_language_code() -> str:
    global __args
    return __args.language_code


def get_clear_cache() -> bool:
    global __args
    return __args.clear_cache


def get_skip_ports() -> list:
    global __args
    return __args.skipPorts
