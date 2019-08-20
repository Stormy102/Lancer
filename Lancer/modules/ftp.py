from utils import *


def ftp(openport):
    print(warning_message(), serviceName, "is recognised by nmap as a ftp program")
    for script in openport.getElementsByTagName('script'):
        if script.attributes['id'].value == "ftp-anon":
            print(warning_message(), "Anonymous FTP access allowed")
