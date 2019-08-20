#!/usr/bin/env python3

from helpers import *
from messages import *
from shutil import which
from xml.dom import minidom
from spinner import Spinner

import sys
import argparse
import signal
import subprocess
import cpe_utils
import platform
import time

'''
    Handles signal interrupts more gracefully than default behaviour
'''

args = None

def ProgramInstalled(name, critical):
    if which(name) is None:
        if critical:
            print(Color("[!]", "Red"), name, "is not installed, halting...")
            sys.exit(1)
        else:
            print(Color("[*]", "Yellow"), name, "is not installed, skipping...")
            return False

    if args.verbose:
        print (Color("[+]", "Green"), name, "is installed, continuing...")
    return True

def Setup():
    if not os.path.exists("nmap"):
        os.makedirs("nmap")

def DetectService(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        serviceName = service.attributes['name'].value
        print (Color("[+]", "Green"), serviceName, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if args.skipPorts is None or port not in args.skipPorts:
            # Some kind of ftp service
            if serviceName == "ftp":
                print (Color("[*]", "Yellow"), serviceName, "is recognised by nmap as a ftp program")

                for script in openport.getElementsByTagName('script'):
                    if script.attributes['id'].value == "ftp-anon":
                        print (Color("[*]", "Yellow"), "Anonymous FTP access allowed")

                print("")
            # Some kind of SSH server
            if serviceName == "ssh":
                print (Color("[*]", "Yellow"), serviceName, "is recognised by nmap as an ssh server\n")
            # Some kind of http service
            if serviceName == "http":
                print (Color("[*]", "Yellow"), serviceName, "is recognised by nmap as a http program. Will commence enumeration using gobuster and Nikto...\n")
            # Smb share
            if port == 445:
                print (Color("[*]", "Yellow"), serviceName, "is potentially a SMB share on Windows. Will commence enumeration using smbclient...\n")
                Smbclient()
            if serviceName == "mysql":
                print (Color("[*]", "Yellow"), serviceName, "is potentially a MySQL server...\n")
        else:
            print (Color("[*]", "Yellow"), "Skipping", serviceName, "(port", str(port) + ") as it has been specified as a port to skip\n")
            
def Smbclient():
    print (Color("[+]", "Green"), "Using SMBClient to enumerate SMB shares...")
    if ProgramInstalled("smbclient", True):
        print (Color("[+]", "Green"), "Using SMBClient to list available shares...")
        smbclientList = subprocess.check_output(['smbclient','-L', args.target]).decode('UTF-8')
        print(smbclientList)
        print("")

def SearchsploitNmapScan(nmapFile):
    print (Color("[+]", "Green"), "Checking searchsploit for detected version vulnerabilities...")
    if ProgramInstalled("searchsploit", False):
        searchsploitOutput = subprocess.check_output(['searchsploit','--nmap', outFile]).decode('UTF-8')
        print("")
        print(searchsploitOutput)
    print("")

def ParseNmapScan(outFile):
    xmldoc = minidom.parse(outFile)
    hostslist = xmldoc.getElementsByTagName('hosts')
    # We only scan one host at a time
    if int(hostslist[0].attributes['down'].value) > 0:
        print(Color("[!]", "Red"), "Target was unreachable")
    else:
        portlist = xmldoc.getElementsByTagName('port')
        print("")

        print (Color("[+]", "Green"), len(portlist), "ports are open")
        
        cpelist = xmldoc.getElementsByTagName('cpe')
        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_osstr = "cpe:/o"
            if cpe_retrieved.startswith(cpe_osstr):
                print (Color("[+]", "Green"), "Target OS appears to be", cpe_utils.CPE(cpe_retrieved).human())
        
        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_appstr = "cpe:/a"
            if cpe_retrieved.startswith(cpe_appstr):
                print (Color("[+]", "Green"), "Installed application is reported as", cpe_utils.CPE(cpe_retrieved).human())
        
        #if cpe.matches(cpe_utils.CPE("cpe:/o:microsoft:windows")) and platform.system() == "linux":
        #    print (Color("[*]", "Yellow"), "Target machine is running Microsoft Windows. Will commence enumeration using enum4linux")

        # New line for nicer formatting
        print("")
        
        SearchsploitNmapScan(outFile)
        
        for openport in portlist:
            DetectService(openport)

def NmapScan(quiet):
    print(Color("[+]", "Green"), "Starting scan of", args.target)
        
    if args.verbose:
        print (Color("[+]", "Green"), "Checking that nmap is installed")

    # Check if Nmap is installed - critical program
    ProgramInstalled("nmap", True)

    if quiet:
        outFile = "nmap/nmap-%s-quiet.xml" % args.target
        print (Color("[+]", "Green"), "Using quiet scan on", args.target, "to avoid detection")
        print (Color("[+]", "Green"), "Scanning open ports on", args.target, "using nmap with arguments: -sS -sV", args.target, end = ' ')

        if args.verbose:
            print ("\n" + Color("[+]", "Green"), "Writing Nmap data to", outFile, end = ' ')

        with Spinner():
            output = subprocess.check_output(['nmap','-sS', '-sV', '-oX', outFile, args.target]).decode('UTF-8')
    else:
        outFile = "nmap/nmap-%s.xml" % args.target
        print (Color("[+]", "Green"), "Scanning open ports on", args.target, "using nmap with arguments: -sC -sV", args.target, end = ' ')
        
        if args.verbose:
            print (Color("[+]", "Green"), "Nmap data will be written to", outFile)

        with Spinner():
            output = subprocess.check_output(['nmap','-sC', '-sV', '-oX', outFile, args.target]).decode('UTF-8')

    print ("")
    
    if args.show_output:
        print("")
        print(output)

    print (Color("[+]", "Green"), "Scan complete")

    ParseNmapScan(outFile)

def ParseArguments():
    global args
    
    example = 'Examples:\n\n'
    example += '$ python lancer.py -T 10.10.10.100 --verbose\n'
    example += '$ python lancer.py --target-file targets --skip-ports 445 8080 --show-program-output\n'
    example += '$ python lancer.py --target 192.168.1.10 --nmap nmap/bastion.xml /\n  -wW /usr/share/wordlists/dirbuster/directory-2.3-small.txt /\n  -fD HTB -fU L4mpje -fP P@ssw0rd'
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Lancer - system vulnerability scanner\n\nThis tool is designed to aid the recon phase of a pentest or any legal & authorised attack against a device or network. The author does not take any liability for use of this tool for illegal use.", epilog=example)

    mainArgs = parser.add_argument_group("Main arguments")
    mex_group = mainArgs.add_mutually_exclusive_group(required=True)
    mex_group.add_argument("-T", "--target", metavar="TARGET", dest='target', type=str, help="IP of target")
    mex_group.add_argument("--target-file", metavar="FILE", dest="hostfile", type=argparse.FileType('r'), help="File containing a list of target IP addresses")
    mainArgs.add_argument("-q", "--quiet", dest='quiet', action="store_true", default='', help="Do a quiet nmap scan. This will help reduce the footprint of the scan in logs and on IDS which may be present in a network.")
    mainArgs.add_argument("-v", "--verbose", dest='verbose', action="store_true", default='', help="Use a more verbose output. This will output more detailed information and may help to diagnose any issues")
    mainArgs.add_argument("-sd", "--skip-disclaimer", dest='skipDisclaimer', action="store_true", default='', help="Skip the legal disclaimer. By using this flag, you agree to use the program for legal and authorised use")
    mainArgs.add_argument("--skip-ports", nargs='+', type=int, metavar="PORTS", dest='skipPorts', default='', help='Set the ports to ignore. These ports will have no enumeration taken against them, except for the initial discovery via nmap. This can be used to run a custom scan and pass the results to Lancer.')
    mainArgs.add_argument("--show-output", dest='show_output', action="store_true", default='', help="Show the output of the programs which are executed, such as nmap, nikto, smbclient and gobuster")
    mainArgs.add_argument("--nmap", metavar="FILE", dest='nmapFile', type=str, help="Skip an internal nmap scan by providing the path to an nmap XML file")

    sgroup2 = parser.add_argument_group("Web Services", "Options for targeting web services")
    sgroup2.add_argument("-wW", metavar="WORDLIST", dest='webWordlist', default='/usr/share/wordlists/dirbuster/directory-2.3-medium.txt', help="The wordlist to use. Defaults to the directory-2.3-medium.txt file found in /usr/share/wordlists/dirbuster")

    sgroup3 = parser.add_argument_group("File Services", "Options for targeting file services")
    sgroup3.add_argument("-fD", metavar="DOMAIN", dest='fileDomain', help="Domain to use during the enumeration of file services")
    sgroup3.add_argument("-fU", metavar="USERNAME", dest='fileUsername', help="Username to use during the enumeration of file services")
    sgroup3.add_argument("-fP", metavar="PASSWORD", dest='filePassword', help="Password to use during the enumeration of file services")
    
    if len(sys.argv) is 1:
        print(Color("[!]", "Red"), "No arguments supplied, showing help...\n")
        time.sleep(0.5)
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    # Display the splash screen
    SplashScreen()
    # Legal disclaimer
    if args.skipDisclaimer is not True:
        print(Color("[!]", "Red"), "Legal Disclaimer: Usage of Lancer for attacking targets without prior mutual authorisation is illegal.\n    It is the end user's responsibility to adhere to all local and international laws.\n    The developer(s) of this tool assume no liability and are not responsible for any misuse or damage caused by the use of this program")
        agree = input(Color("[>]", "Purple") +  " Press [Y] to agree: ")
        if agree.lower() != "y":
            print(Color("[!]", "Red"), "Legal disclaimer has not been accepted. Exiting...")
            sys.exit(0)
    
    # If we have passed an nmap xml file
    if args.nmapFile is not None:
        print(Color("[+]", "Green"), "Loading nmap file")
        ParseNmapScan(args.nmapFile)
    else:
        if args.quiet:
            NmapScan(True)
        else:
            NmapScan(False)

def SignalHandler(signal, frame):
    print(Color("[!]", "Red"), "Ctrl+C detected, terminating...")
    sys.exit(1)

def Main():
    # Register the signal handler for a more graceful Ctrl+C
    signal.signal(signal.SIGINT, SignalHandler)

    # Check if we are on Windows 10 and if we have the VirtualTerminalLevel set to 1
    if IsNotVirtualTerminal():
        print ("\n[*] To enable output colouring in the console, we need to set a registry value (HKCU\\Console\\VirtualTerminalLevel). Do you wish to continue? [Y/N]")
        if input("> ").lower() == "y":
            SetVirtualTerminal()

    # Run the setup to make sure necessary files and permissions exist
    Setup()
    # Parse the arguments
    ParseArguments()

    print(Color("[+]", "Green"), "Lancer has finished system scanning")
    
    sys.exit(0)
    
if __name__ == "__main__":
    #try:
    Main()
    #except:
    #    print(Color("[!]", "Red"), "An unexpected error has occured")
