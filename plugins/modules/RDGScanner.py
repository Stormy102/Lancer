# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

# This is an adaptation of the following script:
# https://github.com/MalwareTech/RDGScanner/blob/master/RDGScanner.py

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot
from OpenSSL import SSL
from OpenSSL._util import (lib as _lib)

import socket
import struct
import select


class RDGScanner(BaseModule):

    def __init__(self):
        super(RDGScanner, self).__init__(name="RDG Scanner",
                                         description="Scans for CVE 2020-0609/0610",
                                         loot_name="rdg-scanner",
                                         intrusion_level=3)
        self.DTLSv1_METHOD = 7
        SSL.Context._methods[self.DTLSv1_METHOD] = getattr(_lib, "DTLSv1_client_method")
        self.vulnerable = True
        self.connected = False

    def execute(self, ip: str, port: int) -> None:
        """
        Scan to check if the target device is vulnerable to MS17-010
        :param ip: The IP to scan
        :param port: The port to use
        """
        self.create_loot_space(ip, port)

        self.scan_server(ip, port, 3)

        if self.connected:
            if self.vulnerable:
                msg = "Likely vulnerable to CVE 2020-0609/0610"
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.warning(msg)
            else:
                msg = "Doesn't appear vulnerable to CVE 2020-0609/0610"
                Loot.loot[ip][str(port)][self.loot_name] = msg
                self.logger.info(msg)
        else:
            msg = "Unable to connect to {IP}:{PORT} - might not be running RDP Gateway server".format(IP=ip, PORT=port)
            Loot.loot[ip][str(port)][self.loot_name] = msg
            self.logger.info(msg)

    def scan_server(self, ip, port, timeout):

        self.logger.log('Checking {IP}:{PORT}'.format(IP=ip, PORT=port))

        ctx = SSL.Context(self.DTLSv1_METHOD)
        ctx.set_verify_depth(2)
        ctx.set_verify(SSL.VERIFY_PEER, self.certificate_callback)

        sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

        sock.connect((ip, int(port)))
        sock.send(self.build_connect_packet(0, 65, b"A"))

        read_fds, _, _ = select.select([sock], [], [], timeout)
        if read_fds:
            data = sock.recv(1024)
            if len(data) == 16:
                error_code = struct.unpack('<L', data[12:])[0]
                if error_code == 0x8000ffff:
                    self.vulnerable = False

    def build_connect_packet(self, fragment_id, num_fragments, data):
        packet_type = 5
        packet_len = len(data) + 6
        fragment_id = fragment_id
        num_fragments = num_fragments
        fragment_len = len(data)
        data = data

        packet = struct.pack('<HHHHH', packet_type, packet_len, fragment_id,
                             num_fragments, fragment_len)
        packet += data
        self.logger.log("Created connection packet")
        return packet

    def certificate_callback(self, sock, cert, err_num, depth, ok):

        server_name = cert.get_subject().commonName
        print('Got certificate for server: %s' % server_name)

        self.connected = True
        return True

    def should_execute(self, service: str, port: int) -> bool:
        if not super(RDGScanner, self).should_execute(service, port):
            return False
        if port == 3391:
            return True
        return False
