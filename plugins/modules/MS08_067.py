# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

# With thanks to
# - https://labs.portcullis.co.uk/tools/ms08-067-check/
# - https://labs.f-secure.com/assets/BlogFiles/hello-ms08-067-my-old-friend.pdf
# - https://github.com/pwnieexpress/metasploit-framework/blob/master/modules/auxiliary/scanner/smb/ms08_067_check.rb
# - For providing the included NDR classes/functions https://github.com/daemitus/pymsrpc

from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot
from impacket import smb, smbconnection, uuid, nmb
from impacket.dcerpc.v5 import transport
from string import ascii_letters
from random import choice

import struct
import socket


class MS08_067(BaseModule):

    def __init__(self):
        super(MS08_067, self).__init__(name="MS08-067 Scanner",
                                       description="Scans for MS08-067/CVE 2008-4250",
                                       loot_name="ms08-067",
                                       intrusion_level=5)

    def execute(self, ip: str, port: int) -> None:
        """
        Scan to see if the target computer is vulnerable to MS08-067
        :param ip: The IP to use
        :param port: The port to use
        """
        self.create_loot_space(ip, port)

        try:
            self.logger.debug("Attempting to connect anonymously via RPC")
            trans = transport.DCERPCTransportFactory('ncacn_np:%s[\\pipe\\browser]' % ip)
            trans.connect()
        except smb.SessionError:
            self.logger.error("Access denied - RestrictAnonymous is probably set to 2")
            return
        except smbconnection.SessionError as e:
            self.logger.error("Session Error: " + e.getErrorString()[0])
            return

        try:
            self.logger.debug("Getting DCE bind")
            dce = trans.DCERPC_class(trans)
            dce.bind(uuid.uuidtup_to_bin(('4b324fc8-1670-01d3-1278-5a47bf6ee188', '3.0')))
        except socket.error:
            self.logger.error("Unable to bind to SRVSVC endpoint")
            return
        except Exception as e:
            self.logger.error("Unexpected exception: " + str(e))
            return

        # Generate a random path
        path = ''.join([choice(ascii_letters) for _ in range(0, 3)])

        stub = NDRUtils.ndr_unique(pointer_value=0x00020000, data=NDRUtils.ndr_wstring(data='')).serialize()
        stub += NDRUtils.get_ndr_wstring(data='\\%s\\..\\%s' % ('A' * 5, path))
        stub += NDRUtils.get_ndr_wstring(data='\\%s' % path)
        stub += struct.pack("<l", 1)
        stub += struct.pack("<l", 0)

        self.logger.info("Sending " + stub.hex() + " to NetPathCanonicalize")

        dce.call(32, stub)  # NetPathCanonicalize
        try:
            resp = dce.recv()
        except nmb.NetBIOSTimeout:
            self.logger.error("NetBIOS connection timed out - this could be due to the OS being Windows XP SP2/3, in"
                              " which scanning can lead to a race condition and heap corruption in the svchost.exe"
                              " process, ultimately causing the process to crash")
            return

        vulnerable = struct.pack('<L', 0)
        # The target is vulnerable if the NetprPathCompare response field
        # 'Windows Error' is WERR_OK (0x00000000)
        if resp == vulnerable:
            msg = "Likely vulnerable to MS08-067/CVE 2008-4250. Received response: WERR_OK ({RESPONSE})" \
                .format(RESPONSE=resp.hex())
            Loot.loot[ip][str(port)][self.loot_name] = msg
            self.logger.warning(msg)
        else:
            msg = "Does not appear vulnerable to MS08-067/CVE 2008-4250. Received response: {RESPONSE}" \
                .format(RESPONSE=resp.hex())
            Loot.loot[ip][str(port)][self.loot_name] = msg
            self.logger.info(msg)

    def should_execute(self, service: str, port: int) -> bool:
        if not super(MS08_067, self).should_execute(service, port):
            return False
        if "microsoft-ds" in service:
            return True
        if port == 445:
            return True
        return False


# TODO: Transition from the legacy PyMSRPC classes to the newer impacket classes
class NDRUtils(object):
    def get_ndr_wstring(data: str):
        align_byte = b"\xaa"

        # Add our wide null because it gets counted
        data = data.encode("utf-16le") + b"\x00\x00"

        length = int(len(data) / 2)
        pad = align_byte * ((4 - (len(data) & 3)) & 3)
        return struct.pack("<L", length) \
               + struct.pack("<L", 0) \
               + struct.pack("<L", length) \
               + data \
               + pad

    class ndr_container(object):
        def __init__(self):
            self.d = None
            self.s = None
            self.parent = None
            self.align_byte = None

        def align(self, data):
            return self.align_byte * ((4 - (len(data) & 3)) & 3)

        def add_static(self, obj):
            if not self.parent:
                self.s.append(obj)
            else:
                self.parent.add_static(obj)

        def add_deferred(self, obj):
            if not self.parent:
                self.d.append(obj)
            else:
                self.parent.add_deferred(obj)

        def serialize(self):
            raise NotImplementedError

    class ndr_primitive(object):
        def align(self, data):
            return self.align_byte * ((4 - (len(data) & 3)) & 3)

        def serialize(self):
            raise NotImplementedError

    class ndr_pad(ndr_primitive):
        """
            pad placeholder
        """

        def __init__(self):
            pass

    class ndr_unique(ndr_container):
        def __init__(self, data: str = "", align_byte: str = b"\xaa", pointer_value: int = 0x41424344):
            self.data = data
            self.align_byte = align_byte
            self.pointer_value = pointer_value
            self.size = 4
            self.alignment = 4

            self.parent = None
            self.s = []
            self.d = []

        def serialize(self):
            self.add_static(NDRUtils.ndr_long(data=self.pointer_value))

            if isinstance(self.data, NDRUtils.ndr_container):
                self.data.parent = self

            self.add_deferred(self.data)

            if not self.parent:
                while len(self.d):
                    d = self.d.pop(0)
                    if isinstance(d, NDRUtils.ndr_container):
                        d.serialize()
                    else:
                        self.add_static(d)

                serialdata = b""
                for s in self.s:
                    if isinstance(s, NDRUtils.ndr_pad):
                        serialdata += self.align(serialdata)
                    else:
                        serialdata += s.serialize()

                self.parent = None
                self.s = []
                self.d = []

                return serialdata

    class ndr_wstring(ndr_primitive):
        """
            encode: wchar *element_1;
        """

        def __init__(self, data="\\\\VULNSVR", align_byte=b"\xaa"):
            self.data = data
            self.align_byte = align_byte
            self.size = 0

        def pad(self, data):
            return self.align_byte * ((4 - (len(data) & 3)) & 3)

        def serialize(self):
            # Add our wide null because it gets counted
            data = self.data.encode("utf-16le") + b"\x00\x00"

            length = int(len(data) / 2)
            pad = self.pad(data)

            return struct.pack("<L", length) \
                   + struct.pack("<L", 0) \
                   + struct.pack("<L", length) \
                   + data \
                   + pad

    class ndr_long(ndr_primitive):
        """
            encode: long element_1;
        """

        def __init__(self, data=0x00000002, signed=True):
            self.data = data
            self.signed = signed
            self.size = 4

        def serialize(self):
            if self.signed:
                return struct.pack("<l", self.data)
            else:
                return struct.pack("<L", self.data)
