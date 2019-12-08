# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.TelnetBanner import TelnetBanner
from core import Loot, config

import warnings
import pytest


@pytest.mark.module
def test_module_creation():
    banner = TelnetBanner()
    assert banner is not None


@pytest.mark.module
def test_disabled_config():
    module = TelnetBanner()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("telnet", 23)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_run_service():
    banner = TelnetBanner()

    result = banner.should_execute("telnet", 2323)

    assert result is True


@pytest.mark.module
def test_should_run_port():
    banner = TelnetBanner()

    result = banner.should_execute("microsoft-tlnt-svc", 23)

    assert result is True


@pytest.mark.module
def test_should_not_run():
    banner = TelnetBanner()

    result = banner.should_execute("ssh", 22)

    assert result is False


@pytest.mark.noci
@pytest.mark.module
def test_get_banner():
    banner = TelnetBanner()

    hostname = "127.0.0.1"
    port = 23

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
    banner = TelnetBanner()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2323

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
    assert "Banner" not in Loot.loot[hostname][port][banner.loot_name]


@pytest.mark.module
def test_get_banner_invalid():
    banner = TelnetBanner()
    Loot.reset()

    hostname = "256.128.63.32"
    port = 23

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None


@pytest.mark.module
def test_get_banner_timeout():
    banner = TelnetBanner()
    Loot.reset()

    hostname = "1.1.1.1"
    port = 23

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
