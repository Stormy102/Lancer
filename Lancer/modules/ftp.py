from utils import *

import config
import time


def ftp(openport):
    for script in openport.getElementsByTagName('script'):
        if script.attributes['id'].value == "ftp-anon":
            print(warning_message(), "Anonymous FTP access allowed")
            if config.args.quiet is not True:
                print(warning_message(), "Downloading all files under 100mb into ./ftp/...")

                with Spinner():
                    time.sleep(0.5)
                print(error_message(), "Downloading the FTP directory is not yet supported")
