# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.GetHostname import GetHostname
from core import Loot, config

import pytest


@pytest.mark.module
def test_module_creation():
    hostname = GetHostname()
    assert hostname is not None


@pytest.mark.module
def test_should_execute():
    module = GetHostname()
    assert module.should_execute("", 0)


@pytest.mark.module
def test_should_not_execute():
    module = GetHostname()
    assert not module.should_execute("", 21)


@pytest.mark.module
def test_disabled_config():
    module = GetHostname()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("", 0)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_get_valid_hostname():
    hostname = GetHostname()

    ip = "127.0.0.1"

    hostname.execute(ip, 0)

    assert "Hostname" in Loot.loot[ip][hostname.loot_name]
    assert Loot.loot[ip][hostname.loot_name]["Hostname"] is not None


@pytest.mark.module
def test_get_invalid_ip():
    hostname = GetHostname()

    ip = "127.0.0.127"

    hostname.execute(ip, 0)

    assert "Hostname" not in Loot.loot[ip][hostname.loot_name]


@pytest.mark.module
def test_create_loot_space():
    hostname = GetHostname()

    ip = "1.1.1.1"

    hostname.create_loot_space(ip, 0)

    assert Loot.loot[ip] is not None
    assert Loot.loot[ip][hostname.loot_name] is not None
