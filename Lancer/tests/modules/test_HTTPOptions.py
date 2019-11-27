# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.HTTPOptions import HTTPOptions
from core import Loot


def test_module_creation():
    options = HTTPOptions()
    assert options is not None


def test_should_execute_service_http():
    options = HTTPOptions()
    assert options.should_execute("http", 1337) is True


def test_should_execute_service_https():
    options = HTTPOptions()
    assert options.should_execute("ssl/https", 1337) is True


def test_should_execute_service_http_proxy():
    options = HTTPOptions()
    assert options.should_execute("http-proxy", 1337) is True


def test_should_execute_service_https_alt():
    options = HTTPOptions()
    assert options.should_execute("https-alt", 1337) is True


def test_should_execute_port_80():
    options = HTTPOptions()
    assert options.should_execute("web-service", 80) is True


def test_should_execute_port_443():
    options = HTTPOptions()
    assert options.should_execute("web-service", 443) is True


def test_should_execute_port_8008():
    options = HTTPOptions()
    assert options.should_execute("web-service", 8008) is True


def test_should_execute_port_8080():
    options = HTTPOptions()
    assert options.should_execute("web-service", 8080) is True


def test_should_execute_port_8443():
    options = HTTPOptions()
    assert options.should_execute("web-service", 8443) is True


def test_should_not_execute():
    options = HTTPOptions()
    assert options.should_execute("unknown-service", 1337) is False


def test_get_valid_options():
    options = HTTPOptions()

    hostname = "apache.org"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][options.loot_name], list)
    assert "OPTIONS" in Loot.loot[hostname][port][options.loot_name]


def test_get_invalid_options():
    options = HTTPOptions()

    hostname = "www.facepunch.com"
    port = 443

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]


def test_get_invalid_url():
    options = HTTPOptions()

    hostname = "kekekekekekeke.kek"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]


def test_get_bad_url():
    options = HTTPOptions()

    hostname = "https://127.0.0.1/"
    port = 80

    options.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][options.loot_name] is not None
    assert not Loot.loot[hostname][port][options.loot_name]

