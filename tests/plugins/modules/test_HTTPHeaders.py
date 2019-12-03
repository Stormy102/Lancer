# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.HTTPHeaders import HTTPHeaders
from core import Loot, config

import pytest


@pytest.mark.module
def test_module_creation():
    headers = HTTPHeaders()
    assert headers is not None


@pytest.mark.module
def test_disabled_config():
    module = HTTPHeaders()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("http", 80)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_get_http():
    headers = HTTPHeaders()

    hostname = "httpforever.com"
    port = 80

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


@pytest.mark.module
def test_get_https():
    headers = HTTPHeaders()

    hostname = "www.google.com"
    port = 443

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


@pytest.mark.module
def test_get_non_standard():
    headers = HTTPHeaders()

    hostname = "www.facepunch.com"
    port = 8080

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


@pytest.mark.module
def test_get_invalid_url():
    headers = HTTPHeaders()

    hostname = "kekekekekekeke.kek"
    port = 80

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)
