from utils import *

def Smbclient(verbose):
    print (NormalMessage(), "Using SMBClient to enumerate SMB shares...")
    if ProgramInstalled("smbclient", False, verbose):
        print (NormalMessage(), "Using SMBClient to list available shares...")
        smbclientList = subprocess.check_output(['smbclient','-L', args.target]).decode('UTF-8')
        print(smbclientList)
        print("")
