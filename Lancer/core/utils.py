from datetime import datetime
from core.spinner import *
from shutil import which
from http.client import responses

from core import config
import time
import sys
import platform
import os
import ctypes
import socket


def signal_handler(signal: int, frame):
    print("\n" + error_message(), "Ctrl+C detected, terminating...")
    sys.exit(1)


def program_installed(name, critical):
    if config.args.verbose:
        print(normal_message(), "Checking if {PROGRAM} is installed...".format(PROGRAM=name))

    if which(name.lower()) is None:
        if critical:
            print(error_message(), "{PROGRAM} is not installed, halting...\n".format(PROGRAM=name))
            sys.exit(1)
        else:
            print(warning_message(), "{PROGRAM} is not installed, skipping...".format(PROGRAM=name))
            return False

    if config.args.verbose:
        print(normal_message(), "{PROGRAM} is installed, continuing...".format(PROGRAM=name))
    return True


def python_version():
    py_version = sys.version.split()[0]
    if py_version < "3.5":
        print(error_message(), "Unsupported Python version")
        sys.exit(1)


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
        return "36"
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
    # Why this header, you may ask?
    # Well, the header itself depicts a
    # Scout trooper from Star Wars. The
    # purpose of Scout Troopers was to probe
    # enemy defences and reconnoiter, as well
    # as patrol and protect their own base.
    # Elite Scout Troopers were known as Lancers
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
    print(normal_message(), "Initialising Lancer {VERSION} on {OS} {OS_VERSION}".
          format(VERSION=config.__version__,
                 OS=platform.system(),
                 OS_VERSION=platform.release()), end=' ')
    with Spinner():
        time.sleep(1)
    print()
    print(normal_message(), "Starting Lancer at {TIME}"
          .format(TIME=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


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


def is_valid_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False


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
