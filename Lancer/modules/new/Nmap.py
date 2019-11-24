from modules.new.BaseModule import BaseModule

import os
import subprocess
import config


class NmapModule(BaseModule):

    def __init__(self):
        super(NmapModule, self).__init__(name="Nmap",
                                         description="Scans the specified IP address for ports",
                                         loot_name="nmap",
                                         multithreaded=False,
                                         intrusive=True,
                                         critical=True)
        self.required_programs = ["nmap"]

    def should_execute(self, service: str, port: int) -> bool:
        # Nmap scan should always execute
        return True

    def execute(self, ip: str, port: int) -> None:
        out_file = os.path.join(config.nmap_cache(), ("nmap-%s.xml" % config.current_target))

        nmap_args = ['nmap', '-sC', '-sV', '-oX', out_file, config.current_target]

        if config.args.scan_udp:
            # print(utils.normal_message(), "Scanning UDP ports, this may take a long time")
            nmap_args.append('-sU')

        # print(utils.normal_message(), "Scanning open ports on", config.current_target + "...", end=' ')

        # with Spinner():
        output = subprocess.check_output(nmap_args).decode('UTF-8')
