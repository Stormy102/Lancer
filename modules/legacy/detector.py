from modules.legacy import gobuster, nikto

from core import config, utils
import platform
import cpe_utils


def detect_os(cpe_list):
    for cpe in cpe_list:
        cpe_os_type = "cpe:/o"
        if cpe.startswith(cpe_os_type):
            print(utils.normal_message(), "Target OS appears to be", cpe_utils.CPE(cpe).human())
            if cpe_utils.CPE(cpe).matches(cpe_utils.CPE("cpe:/o:microsoft:windows")) \
                    and platform.system() == "linux":
                print(utils.warning_message(), "Target machine is running Microsoft Windows")
                print(utils.warning_message(), "Will commence enumeration using enum4linux")
                print(utils.error_message(), "enum4linux not yet implemented")


def detect_apps(cpe_list):
    for cpe in cpe_list:
        cpe_app_type = "cpe:/a"
        if cpe.startswith(cpe_app_type):
            print(utils.normal_message(), "Installed application is reported as", cpe_utils.CPE(cpe).human())


def detect_service(openport):
    for service in openport.getElementsByTagName('service'):
        port = int(openport.attributes['portid'].value)
        service_type = service.attributes['name'].value
        try:
            service_name = service.attributes['product'].value
        except KeyError:
            service_name = service_type

        print(utils.normal_message(), service_name, "is open on port", port)
        # Ignore the port if its in the list of ports to skip
        if port not in config.args.skipPorts:
            # Some kind of SSH server
            if service_type == "ssh":
                print(utils.warning_message(), service_name, "is recognised by nmap as an ssh server")
                """scripts_ran = service.getElementsByTagName('script')
                for script in scripts_ran:
                    print(script.attributes['id'])
                    if script.attributes['id'] == 'fingerprint-strings':
                        print(script.getElementsByTagName('elem')[0].text)"""
            # Some kind of http service
            if service_type == "http":
                print(utils.warning_message(), service_name, "is recognised by nmap as a http program")
                if not config.args.quiet:
                    print("")
                    url = "http://" + config.current_target + ":" + str(port)
                    # Scan using gobuster
                    gobuster.exec(url)
                    # Scan using nikto
                    nikto.exec(url)
            # Some kind of HTTPS server
            if service_type == "ssl/https" or port == 443:
                print(utils.warning_message(), service_name, "is recognised by nmap as a ssl/https program")
                # See for extracting cert details for hostname leakage https://stackoverflow.com/questions/7689941/
                if not config.args.quiet:
                    print("")
                    url = "http://" + config.current_target + ":" + str(port)
                    # Scan using gobuster
                    gobuster.exec(url)
                    # Scan using nikto
                    nikto.exec(url)
            # MySQL server
            if service_name == "mysql":
                print(utils.warning_message(), service_name, "is recognised by nmap as a MySQL server...")
        else:
            print(utils.warning_message(), "Skipping", service_name, "(port", str(port) + ") as it has been specified "
                                                                                          "as a port to skip")
        print("")
