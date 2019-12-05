# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.FTPBanner import FTPBanner
from core import Loot, config

import warnings
import pytest


@pytest.mark.module
def test_module_creation():
    banner = FTPBanner()
    assert banner is not None


@pytest.mark.module
def test_disabled_config():
    module = FTPBanner()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("ftp", 21)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_run_service():
    banner = FTPBanner()

    result = banner.should_execute("ftp", 2121)

    assert result is True


@pytest.mark.module
def test_should_run_port():
    banner = FTPBanner()

    result = banner.should_execute("ftpd", 21)

    assert result is True


@pytest.mark.module
def test_should_not_run():
    banner = FTPBanner()

    result = banner.should_execute("ssh", 22)

    assert result is False


@pytest.mark.module
def test_get_banner():
    banner = FTPBanner()

    hostname = "speedtest.tele2.net"
    port = 21

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
        warnings.warn("Unable to connect to speedtest.tele2.net")


@pytest.mark.module
def test_get_banner_unreachable():
    banner = FTPBanner()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2121

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
    assert "Banner" not in Loot.loot[hostname][port][banner.loot_name]


@pytest.mark.module
def test_get_banner_invalid():
    banner = FTPBanner()
    Loot.reset()

    hostname = "256.128.63.32"
    port = 21

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None


@pytest.mark.module
def test_get_banner_timeout():
    banner = FTPBanner()
    Loot.reset()

    hostname = "1.1.1.1"
    port = 21

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
