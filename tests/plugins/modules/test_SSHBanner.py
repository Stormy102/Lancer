# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.SSHBanner import SSHBanner
from core import Loot, config

import warnings
import pytest


@pytest.mark.module
def test_module_creation():
    banner = SSHBanner()
    assert banner is not None


@pytest.mark.noci
@pytest.mark.module
def test_get_banner():
    banner = SSHBanner()

    hostname = "127.0.0.1"
    port = 22

    try:
        banner.execute(hostname, port)

        port = str(port)

        assert Loot.loot[hostname] is not None
        assert Loot.loot[hostname][port] is not None
        assert Loot.loot[hostname][port][banner.loot_name] is not None

        if not Loot.loot[hostname][port][banner.loot_name]:
            warnings.warn("Banner not present")
            raise AssertionError()
        assert Loot.loot[hostname][port][banner.loot_name] is not None
    except AssertionError:
        warnings.warn("Unable to connect to local SSH server")


@pytest.mark.module
def test_get_banner_unreachable():
    banner = SSHBanner()
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
    banner = SSHBanner()
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
    banner = SSHBanner()
    Loot.reset()
    config.config["Main"]["Timeout"] = "5"

    hostname = "1.1.1.1"
    port = 22

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
