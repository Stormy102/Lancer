# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

    This is the config module.
    This holds all of the key information which should be accessed globally across Lancer.
"""

from shutil import get_terminal_size
from http.client import responses

import core.config
import time
import sys
import platform
import os
import ctypes
import socket
import textwrap


def signal_handler(signal: int, frame) -> None:
    """
    Handle the Ctrl+C interrupt
    """
    print("\n" + error_message(), "Ctrl+C detected, terminating...")
    sys.exit(1)


def python_version() -> None:
    """
    Check that the Python version is supported
    """
    py_version = sys.version.split()[0]
    if py_version < "3.5":
        print(error_message(), "Unsupported Python version")
        sys.exit(1)


def normal_message() -> str:
    """
    Generates an info prefix string, which is a green [+]
    :return: Formatted string
    """
    return color("[+]", "Green")


def warning_message() -> str:
    """
    Generates a warning prefix string, which is a yellow [*]
    :return: Formatted string
    """
    return color("[*]", "Yellow")


def error_message():
    """
    Generates an error prefix string, which is a red [!]
    :return: Formatted string
    """
    return color("[!]", "Red")


def input_message(message: str) -> str:
    """
    Generates an input prefix string, is a purple [>]
    :param message: The message you want to display to the user
    :return: Text entered into the input
    """
    print(color("[>]", "Purple") + " " + message, end=' ')
    return input()


def color(string: str, foreground: str = None, background: str = None, style: str = None) -> str:
    """
    This function styles the output to the specified format, background and foreground colours

    :param string: The string which needs formatting
    :param style: Takes either bold, underline, negative1 or negative2. If no value is supplied, it defaults to normal
    :param foreground: Takes either red, green, yellow, blue, purple, cyan or black. If no value is supplied, it
     defaults to white
    :param background: Takes either red, green, yellow, blue, purple, cyan or white. If no value is supplied, it
    defaults to black
    :return: The formatted string with the requested attributes
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


def get_text_style(style: str) -> str:
    """
    Get the value for the corresponding style value
    :param style: The style you want - either "bold", "underline", "negative1" or "negative2"
    :return: The style value to format
    """
    style = style.lower()
    styles = {
        "bold": "1",
        "underline": "2",
        "negative1": "3",
        "negative2": "5"
    }
    if style in styles:
        return styles[style]
    return "0"


def get_foreground_color(foreground: str) -> str:
    """
    Get the value for the corresponding foreground value
    :param foreground: The colour you want - either "red", "green", "yellow", "blue", "purple", "cyan", "black" or
    "white"
    :return: The foreground value to format
    """
    foreground = foreground.lower()
    foreground_colours = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "purple": "35",
        "cyan": "36",
        "black": "30"
    }
    if foreground in foreground_colours:
        return foreground_colours[foreground]
    return "37"


def get_background_color(background: str) -> str:
    """
    Get the value for the corresponding foreground value
    :param background: The colour you want - either "red", "green", "yellow", "blue", "purple", "cyan", "black" or
    "white"
    :return: The background value to format
    """
    background = background.lower()
    background_colours = {
        "red": "41",
        "green": "42",
        "yellow": "43",
        "blue": "44",
        "purple": "45",
        "cyan": "46",
        "white": "47"
    }
    if background in background_colours:
        return background_colours[background]
    return "40"


def print_header() -> None:
    """
    Print the header
    """
    # Why this header, you may ask?
    # Well, the header itself depicts a
    # Scout trooper from Star Wars. The
    # purpose of Scout Troopers was to probe
    # enemy defences and reconnoiter, as well
    # as patrol and protect their own base.
    # Elite Scout Troopers were known as Lancers
    header = ""
    header += "            `.--:::::::::::::::::---.              \n"
    header += "          `-::----.............-----::/:.          \n"
    header += "         ./:----.............---------::/:         \n"
    header += "      ``.......--------------------......-..``     \n"
    header += "     ....://+//::------/:o:+.------:::///::-..-    \n"
    header += "     -../+++/:--...``../:o:+...```..--://+//:..`   \n"
    header += "    .-.-//+/:-.........:-/-:..........-://///-..   \n"
    header += "    :..:/++/:-....................------:///:-..   \n"
    header += "    /../+++/-.--------------------------:////-.-   \n"
    header += "    +../+++/:::/osyhddmNNMMMNNNmddhyso+/:////:.-   \n"
    header += "    /../://shmNNNNNNNNNNNMMNNNNNNNNNNNNNNy:/::.-   \n"
    header += "   /...://:NNNNNNNNNNNNNdhhmNNNNNNMNNNNNNN//-:...  \n"
    header += " `-+-..::/:NNNNNNNNNNh+-----:smNNNNNNNNNNm:/-:..-  \n"
    header += " -+s-..::+/hNNNNNNNNo-:+yyoy+-:hNNNNNNNNN+::::..:. \n"
    header += ".:dm:..-////NNNNNNd:-.:-....-:-:sNNNNNNNs-/:::..y:`\n"
    header += "-+NMo..-//+:/dNNNh------...------oNNNNm+-/:/:-.:m/.\n"
    header += "-+NMh-../++/:-/so-----.-+o+/.-----+dds--::+/:-.sN+.\n"
    header += "./hMN:../++/:--------.ydsosyd/-----:----:++/:..md+.\n"
    header += "`-/oo:..:+++:-------.+d/++++sN---------:+++/-./h+: \n"
    header += "  ..-::.-+o+/-------.oh////+oN:-------:/++++../:.` \n"
    header += "     `/:-////-------.oh///++oN:-:::::::/++++--`    \n"
    header += "      .:------------.oh+++++oN--::::---:::::       \n"
    header += "       /------------.ohooooosM--::::-------.       \n"
    header += "       ::-----------.ohooooosN-::::-------:`       \n"
    header += "       `------------.oh+oo+oyN-::::------::        \n"
    header += "           `..-------ohoyyyssM-::::----..`         \n"
    header += "               `.----oddmmmdhM-:::-.`              \n"
    header += "                  `.-odydmmhyM-:.                  \n"
    header += "                     `..-----.`                    \n"

    term_size = get_terminal_size((80, 24))

    header = '\n'.join(x.center(term_size.columns) for x in header.splitlines())
    header += '\n'

    for c in header:
        sys.stdout.write(c)
        sys.stdout.flush()
        if c is '\n':
            time.sleep(0.005)


def display_header() -> None:
    """
    Show the header and the version
    """
    show_header = core.config.config['Main']['ShowHeader']
    if show_header != 'no':
        print_header()
    print(normal_message(), "Initialising Lancer {VERSION} on {OS} {OS_VERSION}".
          format(VERSION=core.config.__version__,
                 OS=platform.system(),
                 OS_VERSION=platform.release()))
    print()


def terminal_width_string(text: str) -> str:
    """
        Formats the given text to fit into the current terminal window size
        :param text: The text you want to format
        :return: The formatted string
    """
    term_size = get_terminal_size((80, 24))
    width = term_size.columns - 4
    resultant_array = textwrap.wrap(text, width)
    # 4 characters for "[+] " padding
    return "\n    ".join(resultant_array)


def clear_screen() -> None:
    """
    Clear the screen
    """
    print("\033[H\033[J")


def get_http_code(code: int) -> str:
    """
    Get the human-readable format of the given HTTP code
    :param code: The code to get the format of
    :return: The human-readable string
    """
    try:
        return responses[code]
    except KeyError:
        return "Unknown Response"


def is_valid_target(target: str):
    """
    Check if the target is valid
    :param target: IP address
    :return: Bool if the target is reachable
    """
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False


def is_user_admin() -> bool:
    """
    Checks if the program is running with elevated privileges

    Taken from https://stackoverflow.com/questions/1026431/cross-platform-way-to-check-admin-rights-in-a-python-script-under-windows

    :return: True if running with elevated privileges
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        print(error_message(), "Unable to determine if Lancer is running with elevated privileges ")
    return False
