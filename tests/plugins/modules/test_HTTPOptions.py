# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.HTTPOptions import HTTPOptions
from core import Loot, config

import pytest


@pytest.mark.module
def test_module_creation():
    options = HTTPOptions()
    assert options is not None


@pytest.mark.module
def test_disabled_config():
    module = HTTPOptions()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("http", 80)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_get_valid_options():
    options = HTTPOptions()

    hostname = "apache.org"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][options.loot_name], list)
    assert "OPTIONS" in Loot.loot[hostname][port][options.loot_name]


@pytest.mark.module
def test_get_invalid_options():
    options = HTTPOptions()

    hostname = "www.facepunch.com"
    port = 443

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]


@pytest.mark.module
def test_get_invalid_url():
    options = HTTPOptions()

    hostname = "kekekekekekeke.kek"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]


@pytest.mark.module
def test_get_invalid_response_code():
    options = HTTPOptions()

    hostname = "www.google.com/teapot"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]


@pytest.mark.module
def test_get_bad_url():
    options = HTTPOptions()

    hostname = "https://127.0.0.1/"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]

