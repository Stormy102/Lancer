# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.SSHAuthMethods import SSHAuthMethods
from core import Loot

import pytest


@pytest.mark.module
def test_module_creation():
    module = SSHAuthMethods()
    assert module is not None

@pytest.mark.module
def test_get_banner_unreachable():
    module = SSHAuthMethods()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2222

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None
    assert "Banner" not in Loot.loot[hostname][port][module.loot_name]


@pytest.mark.module
def test_get_banner_invalid():
    module = SSHAuthMethods()
    Loot.reset()

    hostname = "256.128.63.32"
    port = 22

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None


@pytest.mark.module
def test_get_banner_timeout():
    module = SSHAuthMethods()
    Loot.reset()

    hostname = "1.1.1.1"
    port = 22

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None