import utils

import config
import subprocess


def exec():
    print(utils.normal_message(), "Using SMBClient to enumerate SMB shares...")
    if utils.program_installed("SMBClient", False):
        print(utils.error_message(), "SMBClient is not yet supported")
        # print(normal_message(), "Using SMBClient to list available shares...")
        # smbclient_list = subprocess.check_output(['smbclient', '-g', '-L', config.current_target]).decode('UTF-8')
        # print(smbclient_list)
        print("")