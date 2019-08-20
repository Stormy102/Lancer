from utils import *


def ftp(openport):
    for script in openport.getElementsByTagName('script'):
        if script.attributes['id'].value == "ftp-anon":
            print(warning_message(), "Anonymous FTP access allowed")
