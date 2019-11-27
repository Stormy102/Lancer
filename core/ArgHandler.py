import argparse
from core import config, utils
import sys
import time


def parse_arguments(args):
    parser = create_parser()

    if len(args) is 0:
        utils.display_header()
        print(utils.error_message(), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)

    if len(args) is 1 and args[0] == "--version":
        utils.display_header()
        print(utils.normal_message(), "Lancer {VERSION}".format(VERSION=config.__version__))
        sys.exit(0)

    utils.display_header()

    config.args = parser.parse_args(args)


def create_parser():
    example = 'Examples:\n\n'
    example += '$ python lancer.py -T 10.10.10.100 --verbose\n'
    example += '$ python lancer.py --target-file targets --skip-ports 445 8080 --show-program-output\n'
    example += '$ python lancer.py --target 192.168.1.10 --nmap nmap/bastion.xml /' \
               '\n  -wW /usr/share/wordlists/dirbuster/directory-2.3-small.txt'

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Lancer - system vulnerability scanner\n\nThis tool is designed to"
                                                 " aid the recon phase of a pentest or any legal & authorised attack"
                                                 " against a device or network. The author does not take any liability"
                                                 " for use of this tool for illegal use.\n\n"
                                                 "See the config.ini file for more options"
                                                 " " + config.get_config_path(), epilog=example)

    main_args = parser.add_argument_group("Main arguments")
    mex_group = main_args.add_mutually_exclusive_group(required=True)
    mex_group.add_argument("-T", "--target", metavar="TARGET", dest='target', type=str, help="IP of target")
    mex_group.add_argument("--target-file", metavar="FILE", dest="host_file", type=argparse.FileType('r'),
                           help="File containing a list of target IP addresses")
    main_args.add_argument("-q", "--quiet", dest='quiet', action="store_true", default='',
                           help="[Not yet implemented] Do a quiet nmap scan. This will help reduce the footprint of the"
                                " scan in logs and on IDS which may be present in a network.")
    main_args.add_argument("-v", dest='verbose', action="store_true", default='',
                           help="Use a verbose output. This will output results and information as modules run, which"
                                " can be useful if you don't wish to wait for a report at the end.")
    main_args.add_argument("-vv", dest='very_verbose', action="store_true", default='',
                           help="Use a very verbose output. This will output virtually every single action that Lancer"
                                " makes. Useful for debugging.")
    main_args.add_argument("--cache-root", metavar="PATH", dest='cache_root', default='',
                           help="[Not yet implemented] The root of the cache. This is where all of the data for the"
                                " programs run is stored, which may be useful if you wish to document or save all of"
                                " the data cleanly.")
    main_args.add_argument("--skip-ports", nargs='+', type=int, metavar="PORTS", dest='skipPorts', default=[],
                           help="[Not yet implemented] Set the ports to ignore. These ports will have no enumeration"
                                " taken against them, except for the initial discovery via nmap. This can be used to"
                                " run a custom scan and pass the results to Lancer.")
    main_args.add_argument("--show-output", dest='show_output', action="store_true", default='',
                           help="[Not yet implemented] Show the output of the programs which are executed, such as"
                                " nmap, nikto, smbclient and gobuster")
    main_args.add_argument("-l", "--language", metavar="LANGUAGE", dest='language_code', default='en', type=str,
                           help="[Not yet implemented] Language you want Lancer to run in. Defaults to English (en-GB)")
    main_args.add_argument("--nmap", metavar="FILE", dest='nmapFile', type=str,
                           help="Skip an internal nmap scan by providing the path to an nmap XML file.")
    main_args.add_argument("--version", dest='show_version', action="store_true", default='',
                           help="Shows the current version of Lancer")
    main_args.add_argument("--udp", dest='scan_udp', action="store_true", default='',
                           help="[Not yet implemented] Scan for UDP ports as well as TCP when using nmap. This will"
                                " look for more ports but will result in a much longer scan time")

    web_services = parser.add_argument_group("Web Services", "Options for targeting web services")
    web_services.add_argument("-wW", "--web-wordlist", metavar="WORDLIST", dest='webWordlist', default='',
                              help="[Not yet implemented] The wordlist to use. The default wordlist can be changed in"
                                   " the config file")
    return parser
