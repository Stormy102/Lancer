import time, sys, platform, os

def RunningInIDLE():
    '''
        Returns True if we are within IDLE
    '''
    return 'idlelib.run' in sys.modules

def IsNotVirtualTerminal():
    '''
        If we are on Windows 10, check if the VirtualTerminalLevel value is 1
    '''
    if platform.system().lower() == "windows" and platform.release() == "10":
		import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0, winreg.KEY_READ) as registry_key:
            try:
                value = winreg.QueryValueEx(registry_key, "VirtualTerminalLevel")
                return value[0] != 1
            except FileNotFoundError:
                return True
    else:
        return False

def SetVirtualTerminal():
    '''
        If we are on Windows 10, set the VirtualTerminalLevel to 1 so we support coloured terminal output
    '''
    if platform.system().lower() == "windows" and platform.release() == "10":
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, "VirtualTerminalLevel", 0, winreg.REG_DWORD, 1)

def ClearScreen():
    '''
        Clears the screen depending on the OS
    '''
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def Color(string, foreground=None, background=None, style=None):
    '''
        This function styles the output to the specified format, background and foreground colours

        style - takes either bold, underline, negative1 or negative2. If no value is supplied, it defaults to normal
        foreground - takes either red, green, yellow, blue, purple, cyan or black. If no value is supplied, it defaults to white
        background - takes either red, green, yellow, blue, purple, cyan or white. If no value is supplied, it defaults to black
    '''
    
    attr = []

    # Firstly, parse text style
    if style:
        if style.lower() == "bold":
            attr.append("1")
        elif style.lower() == "underline":
            attr.append("2")
        elif style.lower() == "negative1":
            attr.append("3")
        elif style.lower() == "negative2":
            attr.append("5")
        else:
            attr.append("0")
    else:
        attr.append("0")

    # Then, parse foreground colour
    if foreground:
        if foreground.lower() == "red":
            attr.append("31")
        elif foreground.lower() == "green":
            attr.append("32")
        elif foreground.lower() == "yellow":
            attr.append("33")
        elif foreground.lower() == "blue":
            attr.append("34")
        elif foreground.lower() == "purple":
            attr.append("35")
        elif foreground.lower() == "cyan":
            attr.append("36")
        elif foreground.lower() == "black":
            attr.append("30")
        else:
            attr.append("37")
    else:
        attr.append("37")

    # Finally, parse background colour
    if background:
        if background.lower() == "red":
            attr.append("41")
        elif background.lower() == "green":
            attr.append("42")
        elif background.lower() == "yellow":
            attr.append("43")
        elif background.lower() == "blue":
            attr.append("44")
        elif background.lower() == "purple":
            attr.append("45")
        elif background.lower() == "cyan":
            attr.append("46")
        elif background.lower() == "white":
            attr.append("47")
        else:
            attr.append("40")
    else:
        attr.append("40")

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

