import platform
from importlib import util
winreg_exists = util.find_spec('winreg')
if winreg_exists:
    import winreg


def update_windows_virtual_terminal() -> None:
    """
    Update the registry path if the Virtual Terminal isn't enabled
    """
    # Check if we are on Windows 10 and if we have the VirtualTerminalLevel set to 1
    if is_not_virtual_terminal():
        print("\n[>] To enable output colouring in the console, we need to set a registry value"
              " (HKCU\\Console\\VirtualTerminalLevel). Do you wish to continue? [Y/N]", end=' ')

        if input().lower() == "y":
            if platform.system().lower() == "windows" and platform.release() == "10":
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0, winreg.KEY_WRITE) as registry_key:
                    winreg.SetValueEx(registry_key, "VirtualTerminalLevel", 0, winreg.REG_DWORD, 1)


def is_not_virtual_terminal() -> bool:
    """
    If we are on Windows 10, check if the VirtualTerminalLevel value is 1
    :return: Bool if the terminal is virtual or not
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
