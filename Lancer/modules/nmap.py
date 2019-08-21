from utils import *
from xml.dom import minidom

from modules.ftp import *
from modules.http import *
from modules.smb import *

import config
import subprocess
import cpe_utils
import platform


def nmap_scan(quiet):
    print(normal_message(), "Starting scan of", config.args.target)

    # Check if Nmap is installed - critical program. If this fails, the program will exit
    program_installed("nmap", True)

    if quiet:
        out_file = "nmap/nmap-%s-quiet.xml" % config.args.target
        print(normal_message(), "Using quiet scan on", config.args.target, "to avoid detection")

        if config.args.verbose:
            print(normal_message(), "Writing nmap data to", out_file)

        print(normal_message(), "Scanning open ports on", config.args.target + "...", end=' ')

        with Spinner():
            output = subprocess.check_output(['nmap', '-sS', '-sV', '-oX', out_file, config.args.target]).decode(
                'UTF-8')
    else:
        out_file = "nmap/nmap-%s.xml" % config.args.target
        print(normal_message(), "Scanning open ports on", config.args.target + "...", end=' ')

        if config.args.verbose:
            print(normal_message(), "Nmap data will be written to", out_file)

        with Spinner():
            output = subprocess.check_output(['nmap', '-sC', '-sV', '-oX', out_file, config.args.target]).decode(
                'UTF-8')

    print("")

    if config.args.show_output:
        print("")
        print(output)

    print(normal_message(), "Scan complete")

    parse_nmap_scan(out_file)


def parse_nmap_scan(out_file):
    xmldoc = minidom.parse(out_file)
    hostslist = xmldoc.getElementsByTagName('hosts')
    # We only scan one host at a time
    if int(hostslist[0].attributes['down'].value) > 0:
        print(error_message(), "Target was unreachable")
        sys.exit(1)
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
                if cpe_utils.CPE(cpe_retrieved).matches(cpe_utils.CPE("cpe:/o:microsoft:windows"))\
                        and platform.system() == "linux":
                    print(warning_message(), "Target machine is running Microsoft Windows."
                                             "Will commence enumeration using enum4linux")

        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_appstr = "cpe:/a"
            if cpe_retrieved.startswith(cpe_appstr):
                print(normal_message(), "Installed application is reported as", cpe_utils.CPE(cpe_retrieved).human())

        # New line for nicer formatting
        print("")

        searchsploit_nmap_scan(out_file)

        for openport in portlist:
            detect_service(openport)


def detect_service(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        service_name = service.attributes['name'].value
        print(normal_message(), service_name, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if port not in config.args.skipPorts:
            # Some kind of ftp service
            if service_name == "ftp":
                print(warning_message(), service_name, "is recognised by nmap as a ftp program")
                ftp(openport)
            # Some kind of SSH server
            if service_name == "ssh":
                print(warning_message(), service_name, "is recognised by nmap as an ssh server")
            # Some kind of http service
            if service_name == "http":
                print(warning_message(), service_name, "is recognised by nmap as a http program. Will commence"
                                                       " enumeration using gobuster and Nikto...")
                print("")
                url = "http://" + config.args.target
                # Scan using gobuster
                gobuster(url)
                # Scan using nikto
                nikto(url)
            # Smb share
            if port == 445:
                print(warning_message(), service_name, "is potentially a SMB share on Windows. Will commence"
                                                       " enumeration using smbclient...")
                smb_client(config.args.verbose)
            if service_name == "mysql":
                print(warning_message(), service_name, "is potentially a MySQL server...")
        else:
            print(warning_message(), "Skipping", service_name, "(port", str(port) + ") as it has been specified as a"
                                                                                    " port to skip")

        print("")


def searchsploit_nmap_scan(nmap_file):
    print(normal_message(), "Checking searchsploit for detected version vulnerabilities...")
    if program_installed("searchsploit", False):
        searchsploit_output = subprocess.check_output(['searchsploit', '--nmap', nmap_file]).decode('UTF-8')
        print("")
        print(searchsploit_output)
    print("")
