from core import winutils

import platform
import pytest


@pytest.mark.core
def test_is_not_virtual_terminal():
    if platform.system().lower() != "windows":
        assert winutils.is_not_virtual_terminal() is False
