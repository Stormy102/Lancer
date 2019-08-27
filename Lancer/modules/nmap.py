from xml.dom import minidom
from modules import detector
from spinner import Spinner

import utils
import config
import subprocess
import os
import sys


def nmap_scan(quiet):
    print(utils.normal_message(), "Starting scan of", config.args.target)

    # Check if Nmap is installed - critical program. If this fails, the program will exit
    utils.program_installed("nmap", True)

    if quiet:
        out_file = os.path.join(config.nmap_cache(), ("nmap-%s-quiet.xml" % config.args.target))
        print(utils.normal_message(), "Using quiet scan on", config.args.target, "to avoid detection")

        if config.args.verbose:
            print(utils.normal_message(), "Writing nmap data to", out_file)

        print(utils.normal_message(), "Scanning open ports on", config.args.target + "...", end=' ')

        with Spinner():
            output = subprocess.check_output(['nmap', '-sS', '-sV', '-oX', out_file, config.args.target]).decode(
                'UTF-8')
    else:
        out_file = os.path.join(config.nmap_cache(), ("nmap-%s.xml" % config.args.target))

        if config.args.verbose:
            print(utils.normal_message(), "Nmap data will be written to", out_file)

        nmap_args = ['nmap', '-sC', '-sV', '-oX', out_file, config.args.target]

        if config.args.scan_udp:
            print(utils.normal_message(), "Scanning UDP ports, this may take a long time")
            nmap_args.append('-sU')

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
        port_list = xmldoc.getElementsByTagName('port')
        print("")

        print(utils.normal_message(), len(port_list), "ports are open")

        cpe_list = [x.firstChild.nodeValue for x in xmldoc.getElementsByTagName('cpe')]

        detector.detect_os(cpe_list)
        detector.detect_apps(cpe_list)

        # New line for nicer formatting
        print("")

        searchsploit_nmap_scan(out_file)

        for open_port in port_list:
            detector.detect_service(open_port)


def searchsploit_nmap_scan(nmap_file):
    print(utils.normal_message(), "Checking searchsploit for detected version vulnerabilities...")
    # TODO: Searchsploit doesn't seem that intelligent with the
    # TODO: nmap file parsing. Loop through each program individually
    # TODO: and pass in the program name extracted from nmap
    if utils.program_installed("searchsploit", False):
        searchsploit_output = subprocess.check_output(['searchsploit', '--nmap', nmap_file]).decode('UTF-8')
        print("")
        print(searchsploit_output)
    print("")
