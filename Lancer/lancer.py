#!/usr/bin/env python3

from utils import *
from xml.dom import minidom

from modules.ftp import *
from modules.smb import *
from modules.nmap import *

import sys
import argparse
import signal
import subprocess
import cpe_utils
import platform
import time

args = None


def detect_service(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        service_name = service.attributes['name'].value
        print(normal_message(), service_name, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if port not in args.skipPorts:
            # Some kind of ftp service
            if service_name == "ftp":
                ftp(openport)
            # Some kind of SSH server
            if service_name == "ssh":
                print(warning_message(), service_name, "is recognised by nmap as an ssh server")
            # Some kind of http service
            if service_name == "http":
                print(warning_message(), service_name, "is recognised by nmap as a http program. Will commence"
                                                       "enumeration using gobuster and Nikto...")
            # Smb share
            if port == 445:
                print(warning_message(), service_name, "is potentially a SMB share on Windows. Will commence"
                                                       " enumeration using smbclient...")
                smb_client(args.verbose)
            if service_name == "mysql":
                print(warning_message(), service_name, "is potentially a MySQL server...")
        else:
            print(warning_message(), "Skipping", service_name, "(port", str(port) + ") as it has been specified as a"
                                                                                    " port to skip")

        print("")


def searchsploit_nmap_scan(nmap_file):
    print(normal_message(), "Checking searchsploit for detected version vulnerabilities...")
    if program_installed("searchsploit", False, args.verbose):
        searchsploit_output = subprocess.check_output(['searchsploit','--nmap', outFile]).decode('UTF-8')
        print("")
        print(searchsploit_output)
    print("")


def parse_nmap_scan(out_file):
    xmldoc = minidom.parse(out_file)
    hostslist = xmldoc.getElementsByTagName('hosts')
    # We only scan one host at a time
    if int(hostslist[0].attributes['down'].value) > 0:
        print(error_message(), "Target was unreachable")
    else:
        portlist = xmldoc.getElementsByTagName('port')
        print("")

        print(normal_message(), len(portlist), "ports are open")
        
        cpelist = xmldoc.getElementsByTagName('cpe')
        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_osstr = "cpe:/o"
            if cpe_retrieved.startswith(cpe_osstr):
                print(normal_message(), "Target OS appears to be", cpe_utils.CPE(cpe_retrieved).human())
        
        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_appstr = "cpe:/a"
            if cpe_retrieved.startswith(cpe_appstr):
                print(normal_message(), "Installed application is reported as", cpe_utils.CPE(cpe_retrieved).human())
        
        #if cpe.matches(cpe_utils.CPE("cpe:/o:microsoft:windows")) and platform.system() == "linux":
        #    print (Color("[*]", "Yellow"), "Target machine is running Microsoft Windows. Will commence enumeration using enum4linux")

        # New line for nicer formatting
        print("")
        
        searchsploit_nmap_scan(out_file)
        
        for openport in portlist:
            detect_service(openport)


def nmap_scan(quiet):
    print(normal_message(), "Starting scan of", args.target)
        
    if args.verbose:
        print (normal_message(), "Checking that nmap is installed")

    # Check if Nmap is installed - critical program
    program_installed("nmap", True, args.verbose)

    if quiet:
        out_file = "nmap/nmap-%s-quiet.xml" % args.target
        print(normal_message(), "Using quiet scan on", args.target, "to avoid detection")
        print(normal_message(), "Scanning open ports on", args.target + "...", end=' ')

        if args.verbose:
            print("\n" + normal_message(), "Writing Nmap data to", out_file, end=' ')

        with Spinner():
            output = subprocess.check_output(['nmap', '-sS', '-sV', '-oX', out_file, args.target]).decode('UTF-8')
    else:
        out_file = "nmap/nmap-%s.xml" % args.target
        print(normal_message(), "Scanning open ports on", args.target + "...", end=' ')
        
        if args.verbose:
            print(normal_message(), "Nmap data will be written to", out_file)

        with Spinner():
            output = subprocess.check_output(['nmap','-sC', '-sV', '-oX', out_file, args.target]).decode('UTF-8')

    print("")
    
    if args.show_output:
        print("")
        print(output)

    print(normal_message(), "Scan complete")

    parse_nmap_scan(out_file)


def parse_arguments():
    global args
    
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
    
    args = parser.parse_args()


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

    # Display the Legal disclaimer
    legal_disclaimer()
    
    # Run the program
    execute()

    print(normal_message(), "Lancer has finished system scanning")
    
    sys.exit(0)


'''
    Handles signal interrupts more gracefully than default behaviour
'''


def signal_handler(signal, frame):
    print(error_message(), "Ctrl+C detected, terminating...")
    sys.exit(1)


def setup():
    if not os.path.exists("nmap"):
        os.makedirs("nmap")

    if is_user_admin() == False:
        print(warning_message(), "Lancer doesn't appear to being run with elevated permissions."
                                 " Some functionality may not work\n")


def legal_disclaimer():
    if args.skipDisclaimer is not True:
        print(error_message(), "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual"
                               " authorisation is illegal.\n    It is the end user's responsibility to adhere to all"
                               " local and international laws.\n    The developer(s) of this tool assume no liability"
                               " and are not responsible for any misuse or damage caused by the use of this program")
        agree = input_message("Press [Y] to agree:")
        if agree.lower() != "y":
            print(error_message(), "Legal disclaimer has not been accepted. Exiting...")
            sys.exit(0)


def execute():
    # If we have passed an nmap xml file
    if args.nmapFile is not None:
        print(normal_message(), "Loading nmap file")
        parse_nmap_scan(args.nmapFile)
    else:
        if args.quiet:
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
