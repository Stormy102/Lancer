# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

# This is a Python 3 port and adaptation of the following script:
# https://github.com/nixawk/labs/blob/master/MS17_010/smb_exploit.py

from plugins.abstractmodules.BaseModule import BaseModule
from ctypes import *
from enum import Enum
from core import Loot

import struct
import socket


class MS17_010(BaseModule):

    def __init__(self):
        super(MS17_010, self).__init__(name="MS17-010",
                                       description="Scans for MS17-010/CVE 2017-0144",
                                       loot_name="ms17-010",
                                       intrusion_level=4)

    def execute(self, ip: str, port: int) -> None:
        """
        Scan to check if the target device is vulnerable to MS17-010
        :param ip: The IP to scan
        :param port: The port to use
        """
        self.create_loot_space(ip, port)

        buffersize = 1024
        timeout = 5.0

        # Send smb request based on socket.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        try:
            client.connect((ip, port))
        except ConnectionRefusedError:
            self.logger.error("Connection refused: likely the target doesn't support SMB")
            return
        except socket.timeout:
            self.logger.error("Connection timed out: target is unreachable")
            return

        # SMB - Negotiate Protocol Request
        try:
            self.logger.debug("Generating Negotiate Proto Request packet")
            raw_proto = MS17_010Utils.negotiate_proto_request()
            client.send(raw_proto)
            client.recv(buffersize)
        except ConnectionResetError:
            self.logger.error("Negotiate Proto Request failed: likely the target doesn't support SMBv1")
            return
        except socket.timeout:
            self.logger.error("Negotiate Proto Request timed out")
            return

        try:
            # SMB - Session Setup AndX Request
            self.logger.debug("Generating Session Setup AndX Request")
            raw_proto = MS17_010Utils.session_setup_andx_request()
            client.send(raw_proto)
            tcp_response = client.recv(buffersize)

            try:
                smb_header = tcp_response[4:36]  # SMB Header: 32 bytes
                smb = SMB_HEADER(smb_header)

                user_id = struct.pack('<H', smb.user_id)
            except ValueError:
                self.logger.error("SMB header returned 0 bytes")
                return

            # parse native_os from Session Setup Andx Response
            session_setup_andx_response = tcp_response[36:]
            native_os = session_setup_andx_response[9:].split(b'\x00')[0]
            self.logger.info("OS is reported as {OS}".format(OS=native_os.decode()))

            # SMB - Tree Connect AndX Request
            self.logger.debug("Generating and sending Tree Connect AndX Request")
            raw_proto = MS17_010Utils.tree_connect_andx_request(ip, user_id)
            ipc = "\\\\{}\\IPC$\x00".format(ip)
            self.logger.debug("Connecting to {}with UID {}".format(ipc, user_id.hex()))
            client.send(raw_proto)
            try:
                tcp_response = client.recv(buffersize)
            except ConnectionResetError:
                self.logger.error("Permission denied/connection reset connecting to " + ipc)
                return
            except socket.timeout:
                self.logger.error("Connecting to " + ipc + "timed out")
                return

            try:
                smb_header = tcp_response[4:36]  # SMB Header: 32 bytes
                smb = SMB_HEADER(smb_header)

                tree_id = struct.pack('<H', smb.tree_id)
                process_id = struct.pack('<H', smb.process_id)
                user_id = struct.pack('<H', smb.user_id)
                multiplex_id = struct.pack('<H', smb.multiplex_id)
            except AttributeError:
                self.logger.error("SMB header returned 0 bytes")
                return

            # SMB - PeekNamedPipe Request
            self.logger.debug("Generating and sending PeekNamedPipe Request")
            raw_proto = MS17_010Utils.peeknamedpipe_request(tree_id, process_id, user_id, multiplex_id)
            client.send(raw_proto)
            tcp_response = client.recv(buffersize)

            smb_header = tcp_response[4:36]
            smb = SMB_HEADER(smb_header)

            nt_status = struct.pack('<BBH', smb.error_class, smb.reserved1, smb.error_code)

            # If the response code is 0xC0000205 - STATUS_INSUFF_SERVER_RESOURCES - this machine is vulnerable
            # If the response code is any of the following, the machine is likely patched:
            # 0xC0000008 - STATUS_INVALID_HANDLE - not vulnerable
            # 0xC0000022 - STATUS_ACCESS_DENIED - not vulnerable

            # TODO: Use struct to convert to little-endian
            nt_status = MS17_010Utils.to_litte_endien(nt_status.hex())

            if nt_status == str(SMBError.STATUS_INSUFF_SERVER_RESOURCES):
                msg = "Likely vulnerable to MS17-010/CVE 2017-0144"
                self.logger.warning(msg)
                Loot.loot[ip][str(port)][self.loot_name] = msg

                # vulnerable to MS17-010, check for DoublePulsar infection
                self.logger.debug("Generating Tran2 Request")
                raw_proto = MS17_010Utils.trans2_request(tree_id, process_id, user_id, multiplex_id)
                client.send(raw_proto)
                tcp_response = client.recv(buffersize)

                smb_header = tcp_response[4:36]
                smb = SMB_HEADER(smb_header)

                if smb.multiplex_id == 0x0051:
                    key = MS17_010Utils.calculate_doublepulsar_xor_key(smb.signature)
                    self.logger.info("Host is likely INFECTED with DoublePulsar! - XOR Key: {}".format(key.decode()))
            else:
                if nt_status == str(SMBError.STATUS_INVALID_HANDLE):
                    msg = "Does not appear vulnerable to MS17-010: returned STATUS_INVALID_HANDLE (Windows 8.1 or" \
                          " earlier)"
                    self.logger.info(msg)
                    Loot.loot[ip][str(port)][self.loot_name] = msg
                elif nt_status == str(SMBError.STATUS_ACCESS_DENIED):
                    msg = "Does not appear vulnerable to MS17-010: returned STATUS_ACCESS_DENIED (Windows 10)"
                    self.logger.info(msg)
                    Loot.loot[ip][str(port)][self.loot_name] = msg
                elif nt_status == str(SMBError.STATUS_SMB_BAD_TID):
                    msg = "Returned STATUS_SMB_BAD_TID - did you try scanning using a loopback IP?"
                    self.logger.info(msg)
                else:
                    msg = "Unable to detect if target is vulnerable to MS17-010: returned {STATUS}"\
                        .format(STATUS=SMBError(nt_status).name)
                    self.logger.info(msg)
                    Loot.loot[ip][str(port)][self.loot_name] = msg
        finally:
            client.close()

    def should_execute(self, service: str, port: int) -> bool:
        if not super(MS17_010, self).should_execute(service, port):
            return False
        if "microsoft-ds" in service:
            return True
        if port == 445:
            return True
        return False


class SMBError(Enum):
    # TODO: Add all SMBError codes
    #       https://github.com/amosavian/FileProvider/blob/master/Sources/SMBTypes/SMBErrorType.swift

    def __str__(self):
        return str(self.value)

    STATUS_INSUFF_SERVER_RESOURCES = "0xc0000205"
    STATUS_INVALID_HANDLE = "0xc0000008"
    STATUS_ACCESS_DENIED = "0xc0000022"
    STATUS_SMB_BAD_TID = "0x00050002"


class SMB_HEADER(Structure):
    """
    SMB Header decoder.
    """

    _pack_ = 1  # Alignment

    _fields_ = [
        ("server_component", c_uint32),
        ("smb_command", c_uint8),
        ("error_class", c_uint8),
        ("reserved1", c_uint8),
        ("error_code", c_uint16),
        ("flags", c_uint8),
        ("flags2", c_uint16),
        ("process_id_high", c_uint16),
        ("signature", c_uint64),
        ("reserved2", c_uint16),
        ("tree_id", c_uint16),
        ("process_id", c_uint16),
        ("user_id", c_uint16),
        ("multiplex_id", c_uint16)
    ]

    def __new__(self, buffer=None):
        return self.from_buffer_copy(buffer)

    def __init__(self, buffer):
        pass


class MS17_010Utils(object):

    @staticmethod
    def generate_smb_proto_payload(*protos):
        """
        Generate SMB Protocol. Packet protos in order.
        """
        hexdata = []
        for proto in protos:
            hexdata.extend(proto)
        return b"".join(hexdata)

    @staticmethod
    def negotiate_proto_request():
        """
        Generate a negotiate_proto_request packet.
        """
        netbios = [
            b'\x00',  # 'Message_Type'
            b'\x00\x00\x54'  # 'Length'
        ]

        smb_header = [
            b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
            b'\x72',  # 'smb_command': Negotiate Protocol
            b'\x00\x00\x00\x00',  # 'nt_status'
            b'\x18',  # 'flags'
            b'\x01\x28',  # 'flags2'
            b'\x00\x00',  # 'process_id_high'
            b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
            b'\x00\x00',  # 'reserved'
            b'\x00\x00',  # 'tree_id'
            b'\x2F\x4B',  # 'process_id'
            b'\x00\x00',  # 'user_id'
            b'\xC5\x5E'  # 'multiplex_id'
        ]

        negotiate_proto_request = [
            b'\x00',  # 'word_count'
            b'\x31\x00',  # 'byte_count'

            # Requested Dialects
            b'\x02',  # 'dialet_buffer_format'
            b'\x4C\x41\x4E\x4D\x41\x4E\x31\x2E\x30\x00',  # 'dialet_name': LANMAN1.0

            b'\x02',  # 'dialet_buffer_format'
            b'\x4C\x4D\x31\x2E\x32\x58\x30\x30\x32\x00',  # 'dialet_name': LM1.2X002

            b'\x02',  # 'dialet_buffer_format'
            b'\x4E\x54\x20\x4C\x41\x4E\x4D\x41\x4E\x20\x31\x2E\x30\x00',  # 'dialet_name3': NT LANMAN 1.0

            b'\x02',  # 'dialet_buffer_format'
            b'\x4E\x54\x20\x4C\x4D\x20\x30\x2E\x31\x32\x00'  # 'dialet_name4': NT LM 0.12
        ]

        return MS17_010Utils.generate_smb_proto_payload(netbios, smb_header, negotiate_proto_request)

    @staticmethod
    def session_setup_andx_request():
        """Generate session setuo andx request.
        """
        netbios = [
            b'\x00',  # 'Message_Type'
            b'\x00\x00\x63'  # 'Length'
        ]

        smb_header = [
            b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
            b'\x73',  # 'smb_command': Session Setup AndX
            b'\x00\x00\x00\x00',  # 'nt_status'
            b'\x18',  # 'flags'
            b'\x01\x20',  # 'flags2'
            b'\x00\x00',  # 'process_id_high'
            b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
            b'\x00\x00',  # 'reserved'
            b'\x00\x00',  # 'tree_id'
            b'\x2F\x4B',  # 'process_id'
            b'\x00\x00',  # 'user_id'
            b'\xC5\x5E'  # 'multiplex_id'
        ]

        session_setup_andx_request = [
            b'\x0D',  # Word Count
            b'\xFF',  # AndXCommand: No further command
            b'\x00',  # Reserved
            b'\x00\x00',  # AndXOffset
            b'\xDF\xFF',  # Max Buffer
            b'\x02\x00',  # Max Mpx Count
            b'\x01\x00',  # VC Number
            b'\x00\x00\x00\x00',  # Session Key
            b'\x00\x00',  # ANSI Password Length
            b'\x00\x00',  # Unicode Password Length
            b'\x00\x00\x00\x00',  # Reserved
            b'\x40\x00\x00\x00',  # Capabilities
            b'\x26\x00',  # Byte Count
            b'\x00',  # Account
            b'\x2e\x00',  # Primary Domain
            b'\x57\x69\x6e\x64\x6f\x77\x73\x20\x32\x30\x30\x30\x20\x32\x31\x39\x35\x00',  # Native OS: Windows 2000 2195
            b'\x57\x69\x6e\x64\x6f\x77\x73\x20\x32\x30\x30\x30\x20\x35\x2e\x30\x00',  # Native OS: Windows 2000 5.0
        ]

        return MS17_010Utils.generate_smb_proto_payload(netbios, smb_header, session_setup_andx_request)

    @staticmethod
    def tree_connect_andx_request(ip, userid):
        """Generate tree connect andx request.
        """

        netbios = [
            b'\x00',  # 'Message_Type'
            b'\x00\x00\x47'  # 'Length'
        ]

        smb_header = [
            b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
            b'\x75',  # 'smb_command': Tree Connect AndX
            b'\x00\x00\x00\x00',  # 'nt_status'
            b'\x18',  # 'flags'
            b'\x01\x20',  # 'flags2'
            b'\x00\x00',  # 'process_id_high'
            b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
            b'\x00\x00',  # 'reserved'
            b'\x00\x00',  # 'tree_id'
            b'\x2F\x4B',  # 'process_id'
            userid,  # 'user_id'
            b'\xC5\x5E'  # 'multiplex_id'
        ]

        ipc = "\\\\{}\IPC$\x00".format(ip)

        tree_connect_andx_request = [
            b'\x04',  # Word Count
            b'\xFF',  # AndXCommand: No further commands
            b'\x00',  # Reserved
            b'\x00\x00',  # AndXOffset
            b'\x00\x00',  # Flags
            b'\x01\x00',  # Password Length
            b'\x1A\x00',  # Byte Count
            b'\x00',  # Password
            ipc.encode(),  # \\xxx.xxx.xxx.xxx\IPC$
            b'\x3f\x3f\x3f\x3f\x3f\x00'  # Service
        ]

        length = len(b"".join(smb_header)) + len(b"".join(tree_connect_andx_request))
        # netbios[1] = '\x00' + struct.pack('>H', length)
        netbios[1] = struct.pack(">L", length)[-3:]

        return MS17_010Utils.generate_smb_proto_payload(netbios, smb_header, tree_connect_andx_request)

    @staticmethod
    def peeknamedpipe_request(treeid, processid, userid, multiplex_id):
        """Generate tran2 request
        """
        netbios = [
            b'\x00',  # 'Message_Type'
            b'\x00\x00\x4a'  # 'Length'
        ]

        smb_header = [
            b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
            b'\x25',  # 'smb_command': Trans2
            b'\x00\x00\x00\x00',  # 'nt_status'
            b'\x18',  # 'flags'
            b'\x01\x28',  # 'flags2'
            b'\x00\x00',  # 'process_id_high'
            b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
            b'\x00\x00',  # 'reserved'
            treeid,
            processid,
            userid,
            multiplex_id
        ]

        tran_request = [
            b'\x10',  # Word Count
            b'\x00\x00',  # Total Parameter Count
            b'\x00\x00',  # Total Data Count
            b'\xff\xff',  # Max Parameter Count
            b'\xff\xff',  # Max Data Count
            b'\x00',  # Max Setup Count
            b'\x00',  # Reserved
            b'\x00\x00',  # Flags
            b'\x00\x00\x00\x00',  # Timeout: Return immediately
            b'\x00\x00',  # Reversed
            b'\x00\x00',  # Parameter Count
            b'\x4a\x00',  # Parameter Offset
            b'\x00\x00',  # Data Count
            b'\x4a\x00',  # Data Offset
            b'\x02',  # Setup Count
            b'\x00',  # Reversed
            b'\x23\x00',  # SMB Pipe Protocol: Function: PeekNamedPipe (0x0023)
            b'\x00\x00',  # SMB Pipe Protocol: FID
            b'\x07\x00',
            b'\x5c\x50\x49\x50\x45\x5c\x00'  # \PIPE\
        ]

        return MS17_010Utils.generate_smb_proto_payload(netbios, smb_header, tran_request)

    @staticmethod
    def trans2_request(treeid, processid, userid, multiplex_id):
        """Generate trans2 request.
        """
        netbios = [
            b'\x00',  # 'Message_Type'
            b'\x00\x00\x4f'  # 'Length'
        ]

        smb_header = [
            b'\xFF\x53\x4D\x42',  # 'server_component': .SMB
            b'\x32',  # 'smb_command': Trans2
            b'\x00\x00\x00\x00',  # 'nt_status'
            b'\x18',  # 'flags'
            b'\x07\xc0',  # 'flags2'
            b'\x00\x00',  # 'process_id_high'
            b'\x00\x00\x00\x00\x00\x00\x00\x00',  # 'signature'
            b'\x00\x00',  # 'reserved'
            treeid,
            processid,
            userid,
            multiplex_id
        ]

        trans2_request = [
            b'\x0f',  # Word Count
            b'\x0c\x00',  # Total Parameter Count
            b'\x00\x00',  # Total Data Count
            b'\x01\x00',  # Max Parameter Count
            b'\x00\x00',  # Max Data Count
            b'\x00',  # Max Setup Count
            b'\x00',  # Reserved
            b'\x00\x00',  # Flags
            b'\xa6\xd9\xa4\x00',  # Timeout: 3 hours, 3.622 seconds
            b'\x00\x00',  # Reversed
            b'\x0c\x00',  # Parameter Count
            b'\x42\x00',  # Parameter Offset
            b'\x00\x00',  # Data Count
            b'\x4e\x00',  # Data Offset
            b'\x01',  # Setup Count
            b'\x00',  # Reserved
            b'\x0e\x00',  # subcommand: SESSION_SETUP
            b'\x00\x00',  # Byte Count
            b'\x0c\x00' + b'\x00' * 12
        ]

        return MS17_010Utils.generate_smb_proto_payload(netbios, smb_header, trans2_request)

    @staticmethod
    def to_litte_endien(str: str):
        big = int.from_bytes(bytes.fromhex(str), "big")
        return "0x" + big.to_bytes((big.bit_length() + 7) // 8, "little").hex()

    @staticmethod
    def calculate_doublepulsar_xor_key(s):
        """
        Calaculate Doublepulsar Xor Key
        """
        x = (2 * s ^ (((s & 0xff00 | (s << 16)) << 8) | (((s >> 16) | s & 0xff0000) >> 8)))
        x = x & 0xffffffff  # this line was added just to truncate to 32 bits
        return x
