from utils import *

import config
import subprocess


def smb_client(verbose):
    print(normal_message(), "Using SMBClient to enumerate SMB shares...")
    if program_installed("smbclient", False, verbose):
        print(normal_message(), "Using SMBClient to list available shares...")
        smbclient_list = subprocess.check_output(['smbclient', '-L', config.args.target]).decode('UTF-8')
        print(smbclient_list)
        print("")
