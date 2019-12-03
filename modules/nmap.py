from xml.dom import minidom
from modules.legacy import detector
from core.spinner import Spinner

from core import config, utils
import subprocess
import os


def nmap_scan():
    print(utils.normal_message(), "Starting scan of", config.current_target)

    # Check if Nmap is installed - critical program. If this fails, the program will exit
    utils.program_installed("nmap", True)

    out_file = os.path.join(config.get_module_cache("nmap", config.current_target), "nmap.xml")

    if config.args.verbose:
        print(utils.normal_message(), "Nmap data will be written to", out_file)

    nmap_args = ['nmap', '-sC', '-sV', '-oX', out_file, config.current_target]

    if config.args.scan_udp:
        print(utils.normal_message(), "Scanning UDP ports, this may take a long time")
        nmap_args.append('-sU')

    print(utils.normal_message(), "Scanning open ports on", config.current_target + "...", end=' ')

    with Spinner():
        output = subprocess.check_output(nmap_args).decode('UTF-8')
    print("")

    # if config.args.show_output:
    #    print("")
    #    print(output)

    print(utils.normal_message(), "Scan complete")

    parse_nmap_scan(out_file)


def parse_nmap_scan(out_file):
    xmldoc = minidom.parse(out_file)
    hostslist = xmldoc.getElementsByTagName('hosts')
    # We only scan one host at a time
    if int(hostslist[0].attributes['down'].value) > 0:
        print(utils.error_message(), config.current_target, "was unreachable")
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
    #       nmap file parsing. Loop through each program individually
    #       and pass in the program name extracted from nmap
    # searchsploit -t [PROGRAM]
    if utils.program_installed("searchsploit", False):
        searchsploit_output = subprocess.check_output(['searchsploit', '--nmap', nmap_file]).decode('UTF-8')
        print()
        print(searchsploit_output)
    print("")
