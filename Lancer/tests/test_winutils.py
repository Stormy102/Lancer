import platform
import winutils


def test_is_not_virtual_terminal():
    if platform.system().lower() != "windows":
        assert winutils.is_not_virtual_terminal() is False
