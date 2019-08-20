from utils import *

def Ftp(openport):
    print (WarningMessage(), serviceName, "is recognised by nmap as a ftp program")
    for script in openport.getElementsByTagName('script'):
        if script.attributes['id'].value == "ftp-anon":
            print (WarningMessage(), "Anonymous FTP access allowed")
