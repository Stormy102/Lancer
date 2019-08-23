from datetime import datetime
from spinner import *
from shutil import which
from http.client import responses

import config
import time
import sys
import platform
import os
import ctypes
import socket

# If we're on Windows, import winreg
if platform.system().lower() == "windows" and platform.release() == "10":
    import winreg

def update_windows_virtual_terminal():
    # Check if we are on Windows 10 and if we have the VirtualTerminalLevel set to 1
    if is_not_virtual_terminal():
        print("\n[>] To enable output colouring in the console, we need to set a registry value"
              " (HKCU\\Console\\VirtualTerminalLevel). Do you wish to continue? [Y/N]", end=' ')

        if input().lower() == "y":
            set_virtual_terminal()


def is_not_virtual_terminal():
    """
        If we are on Windows 10, check if the VirtualTerminalLevel value is 1
    """
    if platform.system().lower() == "windows" and platform.release() == "10":
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0, winreg.KEY_READ) as registry_key:
            try:
                value = winreg.QueryValueEx(registry_key, "VirtualTerminalLevel")
                return value[0] != 1
            except FileNotFoundError:
                return True
    else:
        return False


def set_virtual_terminal():
    """
        If we are on Windows 10, set the VirtualTerminalLevel to 1 so we support coloured terminal output
    """
    if platform.system().lower() == "windows" and platform.release() == "10":
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, "VirtualTerminalLevel", 0, winreg.REG_DWORD, 1)


def program_installed(name, critical):
    if config.args.verbose:
        print(normal_message(), "Checking if", name, "is installed...")

    if which(name.lower()) is None:
        if critical:
            print(error_message(), name, "is not installed, halting...\n")
            sys.exit(1)
        else:
            print(warning_message(), name, "is not installed, skipping...")
            return False

    if config.args.verbose:
        print(normal_message(), name, "is installed, continuing...")
    return True


def normal_message():
    return color("[+]", "Green")


def warning_message():
    return color("[*]", "Yellow")


def error_message():
    return color("[!]", "Red")


def input_message(message):
    print(color("[>]", "Purple") + " " + message, end=' ')
    return input()


def color(string, foreground=None, background=None, style=None):
    """
        This function styles the output to the specified format, background and foreground colours

        style - takes either bold, underline, negative1 or negative2. If no value is supplied, it defaults to normal
        foreground - takes either red, green, yellow, blue, purple, cyan or black. If no value is supplied,
        it defaults to white
        background - takes either red, green, yellow, blue, purple, cyan or white. If no value is supplied,
        it defaults to black
    """

    attr = []

    # Firstly, parse text style
    if style:
        attr.append(get_text_style(style))
    else:
        attr.append("0")

    # Then, parse foreground colour
    if foreground:
        attr.append(get_foreground_color(foreground))
    else:
        attr.append("37")

    # Finally, parse background colour
    if background:
        attr.append(get_background_color(background))
    else:
        attr.append("40")

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def get_text_style(style):
    if style.lower() == "bold":
        return "1"
    elif style.lower() == "underline":
        return "2"
    elif style.lower() == "negative1":
        return "3"
    elif style.lower() == "negative2":
        return "5"
    else:
        return "0"


def get_foreground_color(foreground):
    if foreground.lower() == "red":
        return "31"
    elif foreground.lower() == "green":
        return "32"
    elif foreground.lower() == "yellow":
        return "33"
    elif foreground.lower() == "blue":
        return "34"
    elif foreground.lower() == "purple":
        return "35"
    elif foreground.lower() == "cyan":
        return"36"
    elif foreground.lower() == "black":
        return "30"
    else:
        return "37"


def get_background_color(background):
    if background.lower() == "red":
        return "41"
    elif background.lower() == "green":
        return "42"
    elif background.lower() == "yellow":
        return "43"
    elif background.lower() == "blue":
        return "44"
    elif background.lower() == "purple":
        return "45"
    elif background.lower() == "cyan":
        return "46"
    elif background.lower() == "white":
        return "47"
    else:
        return "40"


def print_header():
    print('''                  `.--:::::::::::::::::---.                 
               `-::----.............-----::/:.              
              ./:----.............---------::/:             
           ``.......--------------------......-..``         
          ....://+//::------/:o:+.------:::///::-..-        
          -../+++/:--...``../:o:+...```..--://+//:..`       
         .-.-//+/:-.........:-/-:..........-://///-..       
         :..:/++/:-....................------:///:-..       
         /../+++/-.--------------------------:////-.-       
         +../+++/:::/osyhddmNNMMMNNNmddhyso+/:////:.-       
         /../://shmNNNNNNNNNNNMMNNNNNNNNNNNNNNy:/::.-       
        /...://:NNNNNNNNNNNNNdhhmNNNNNNMNNNNNNN//-:...      
      `-+-..::/:NNNNNNNNNNh+-----:smNNNNNNNNNNm:/-:..-      
      -+s-..::+/hNNNNNNNNo-:+yyoy+-:hNNNNNNNNN+::::..:.     
     .:dm:..-////NNNNNNd:-.:-....-:-:sNNNNNNNs-/:::..y:`    
     -+NMo..-//+:/dNNNh------...------oNNNNm+-/:/:-.:m/.    
     -+NMh-../++/:-/so-----.-+o+/.-----+dds--::+/:-.sN+.    
     ./hMN:../++/:--------.ydsosyd/-----:----:++/:..md+.    
     `-/oo:..:+++:-------.+d/++++sN---------:+++/-./h+:     
       ..-::.-+o+/-------.oh////+oN:-------:/++++../:.`     
          `/:-////-------.oh///++oN:-:::::::/++++--`        
           .:------------.oh+++++oN--::::---:::::           
            /------------.ohooooosM--::::-------.           
            ::-----------.ohooooosN-::::-------:`           
            `------------.oh+oo+oyN-::::------::            
                `..-------ohoyyyssM-::::----..`             
                    `.----oddmmmdhM-:::-.`                  
                       `.-odydmmhyM-:.                      
                          `..-----.`''')


def version():
    print(color("[+]", "Green"), "Starting Lancer", config.__version__, "on", socket.gethostname(),
          "(" + platform.system(), platform.release() + ")", "at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          end=' ')
    with Spinner():
        time.sleep(1)
    print("")


def line_break(count):
    """
        Prints the specified number of line breaks

        count - the number of line breaks to print
    """

    for i in range(0, count):
        print("")


def get_http_code(code):
    try:
        return responses[code]
    except KeyError:
        return "Unknown Response"


class AdminStateUnknownError(Exception):
    """Cannot determine whether the user is an admin."""
    pass


def is_user_admin():
    """
        Taken from
        https://stackoverflow.com/questions/1026431/cross-platform-way-to-check-admin-rights-in-a-python-script-under-windows
    """
    # type: () -> bool
    """Return True if user has admin privileges.

    Raises:
        AdminStateUnknownError if user privileges cannot be determined.
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError
