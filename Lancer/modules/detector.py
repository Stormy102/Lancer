from modules import ftp
from modules.web import http
from modules import smb

import config
import utils


def detect_service(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        service_name = service.attributes['name'].value
        print(utils.normal_message(), service_name, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if port not in config.args.skipPorts:
            # Some kind of ftp service
            if service_name == "ftp":
                print(utils.warning_message(), service_name, "is recognised by nmap as a ftp program")
                ftp.ftp(openport)
            # Some kind of SSH server
            if service_name == "ssh":
                print(utils.warning_message(), service_name, "is recognised by nmap as an ssh server")
            # Some kind of http service
            if service_name == "http":
                print(utils.warning_message(), service_name, "is recognised by nmap as a http program. Will commence"
                                                       " enumeration using gobuster and Nikto...")
                print("")
                url = "http://" + config.args.target
                # Scan using gobuster
                http.gobuster(url)
                # Scan using nikto
                http.nikto(url)
            # Smb share
            if port == 445:
                print(utils.warning_message(), service_name, "is potentially a SMB share on Windows. Will commence"
                                                       " enumeration using smbclient...")
                smb.smb_client(config.args.verbose)
            if service_name == "mysql":
                print(utils.warning_message(), service_name, "is potentially a MySQL server...")
        else:
            print(utils.warning_message(), "Skipping", service_name, "(port", str(port) + ") as it has been specified "
                                                                                          "as a port to skip")

        print("")