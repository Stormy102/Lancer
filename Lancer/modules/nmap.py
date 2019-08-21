from spinner import Spinner
from xml.dom import minidom
from modules import detector

import utils
import config
import subprocess
import cpe_utils
import platform
import sys


def nmap_scan(quiet):
    print(utils.normal_message(), "Starting scan of", config.args.target)

    # Check if Nmap is installed - critical program. If this fails, the program will exit
    utils.program_installed("nmap", True)

    if quiet:
        out_file = "nmap/nmap-%s-quiet.xml" % config.args.target
        print(utils.normal_message(), "Using quiet scan on", config.args.target, "to avoid detection")

        if config.args.verbose:
            print(utils.normal_message(), "Writing nmap data to", out_file)

        print(utils.normal_message(), "Scanning open ports on", config.args.target + "...", end=' ')

        with Spinner():
            output = subprocess.check_output(['nmap', '-sS', '-sV', '-oX', out_file, config.args.target]).decode(
                'UTF-8')
    else:
        out_file = "nmap/nmap-%s.xml" % config.args.target

        if config.args.verbose:
            print(utils.normal_message(), "Nmap data will be written to", out_file)

        nmap_args = ['nmap', '-sC', '-sV', '-oX', out_file, config.args.target]

        if config.args.scan_udp:
            print(utils.normal_message(), "Scanning UDP ports, this may take a long time")

        print(utils.normal_message(), "Scanning open ports on", config.args.target + "...", end=' ')

        with Spinner():
            output = subprocess.check_output(nmap_args).decode('UTF-8')

    print("")

    if config.args.show_output:
        print("")
        print(output)

    print(utils.normal_message(), "Scan complete")

    parse_nmap_scan(out_file)


def parse_nmap_scan(out_file):
    xmldoc = minidom.parse(out_file)
    hostslist = xmldoc.getElementsByTagName('hosts')
    # We only scan one host at a time
    if int(hostslist[0].attributes['down'].value) > 0:
        print(utils.error_message(), "Target was unreachable")
        sys.exit(1)
    else:
        portlist = xmldoc.getElementsByTagName('port')
        print("")

        print(utils.normal_message(), len(portlist), "ports are open")

        cpelist = xmldoc.getElementsByTagName('cpe')
        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_osstr = "cpe:/o"
            if cpe_retrieved.startswith(cpe_osstr):
                print(utils.normal_message(), "Target OS appears to be", cpe_utils.CPE(cpe_retrieved).human())
                if cpe_utils.CPE(cpe_retrieved).matches(cpe_utils.CPE("cpe:/o:microsoft:windows"))\
                        and platform.system() == "linux":
                    print(utils.warning_message(), "Target machine is running Microsoft Windows."
                                             "Will commence enumeration using enum4linux")

        for cpe in cpelist:
            cpe_retrieved = cpe.firstChild.nodeValue
            cpe_appstr = "cpe:/a"
            if cpe_retrieved.startswith(cpe_appstr):
                print(utils.normal_message(), "Installed application is reported as", cpe_utils.CPE(cpe_retrieved)
                      .human())

        # New line for nicer formatting
        print("")

        searchsploit_nmap_scan(out_file)

        for openport in portlist:
            detector.detect_service(openport)


def searchsploit_nmap_scan(nmap_file):
    print(utils.normal_message(), "Checking searchsploit for detected version vulnerabilities...")
    if utils.program_installed("searchsploit", False):
        searchsploit_output = subprocess.check_output(['searchsploit', '--nmap', nmap_file]).decode('UTF-8')
        print("")
        print(searchsploit_output)
    print("")
