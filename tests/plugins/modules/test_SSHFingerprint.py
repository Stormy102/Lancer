# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.SSHFingerprint import SSHFingerprint
from core import Loot, config

import warnings
import pytest


@pytest.mark.module
def test_module_creation():
    banner = SSHFingerprint()
    assert banner is not None


@pytest.mark.module
def test_get_banner_unreachable():
    banner = SSHFingerprint()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2222

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
    assert "Banner" not in Loot.loot[hostname][port][banner.loot_name]


@pytest.mark.module
def test_get_banner_invalid():
    banner = SSHFingerprint()
    Loot.reset()

    hostname = "256.128.63.32"
    port = 22

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None


@pytest.mark.module
def test_get_banner_timeout():
    banner = SSHFingerprint()
    Loot.reset()

    hostname = "1.1.1.1"
    port = 22

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
