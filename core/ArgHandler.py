import argparse
from core import config, utils
import sys
import time


def parse_arguments(args):
    parser = create_parser()

    if len(args) is 0:
        print(utils.error_message(), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)

    if len(args) is 1 and "--version" in args:
        print(utils.normal_message(), "Lancer {VERSION}".format(VERSION=config.__version__))
        sys.exit(0)

    if len(args) is 1 and "-h" or "--help" in args:
        parser.print_help()
        sys.exit(0)

    config.args = parser.parse_args(args)


def create_parser():
    example = 'Examples:\n'
    example += utils.normal_message() + ' ./lancer -T 10.10.10.100 -v -l de -a 10.8.0.1\n'
    example += utils.normal_message() + ' ./lancer -TF targets.lan -vv --cache-root ./cache/\n'
    example += utils.terminal_width_string(
        utils.normal_message() + ' ./lancer -TN nmap-10.0.0.1.xml --skip-ports 445 80 -L 5'
    )

    description = utils.normal_message() + " Lancer - system vulnerability scanner\n"
    description += utils.terminal_width_string(
        utils.normal_message() + " See the config.ini file at {CONFIG_PATH} for more options."
        .format(CONFIG_PATH=config.get_config_path())
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
                         help="[NOT YET IMPLEMENTED] "
                              "Set the ports to ignore. These ports will have no enumeration taken against them,"
                              " except for the initial discovery via Nmap. This can be used to run a custom scan and"
                              " pass the results to Lancer. Best used in conjunction with -TN/--target-nmap.")

    output = parser.add_argument_group("Output Arguments")
    output.description = "Control the output of Lancer."
    verbose_group = output.add_mutually_exclusive_group(required=False)
    verbose_group.add_argument("-v", "--verbose", dest='verbose', action="store_true", default='',
                               help="Use a verbose output. This will output results and information as modules run,"
                                    " which can be useful if you don't wish to wait for a report at the end.")
    verbose_group.add_argument("-vv", "--very-verbose", dest='very_verbose', action="store_true", default='',
                               help="Use a very verbose output. This will output virtually every single event that"
                                    " Lancer logs. Useful for debugging.")
    output.add_argument("-o", "--output", metavar="FILE", dest="host_file", type=argparse.FileType('w'),
                        help="[NOT YET IMPLEMENTED] "
                             "Output the human-readable contents of the Lancer scan to a file. Best used in "
                             " conjunction with -v/-vv")
    output.add_argument("--version", dest='show_version', action="store_true", default='',
                        help="Shows the current version of Lancer.")

    optional_args = parser.add_argument_group("Optional Arguments")
    optional_args.add_argument("-l", "--language", metavar="LANGUAGE", dest='language_code', default='en', type=str,
                               help="[NOT YET IMPLEMENTED] "
                                    "Language you want Lancer to use in. The  language code uses ISO 639-1. Defaults to"
                                    " English.")

    optional_args.add_argument("-h", "--help", action="store_true", dest='help',
                               help="Shows the different arguments available for Lancer.")

    # TODO: remove obsolete arguments
    obsolete = parser.add_argument_group("Obsolete Arguments")
    obsolete.description = "These arguments will be removed in the next update and will reside in config.ini"
    obsolete.add_argument("--udp", dest='scan_udp', action="store_true", default='',
                          help="Scan for UDP ports as well as TCP when using Nmap. This will look for more ports but"
                               " will result in a much longer scan time")
    obsolete.add_argument("--wordlist", metavar="WORDLIST", dest='webWordlist', default='', help="The wordlist to use.")

    return parser
