# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.HTTPHeaders import HTTPHeaders
from core import Loot


def test_module_creation():
    headers = HTTPHeaders()
    assert headers is not None


def test_should_execute_service_http():
    headers = HTTPHeaders()
    assert headers.should_execute("http", 1337) is True


def test_should_execute_service_https():
    headers = HTTPHeaders()
    assert headers.should_execute("ssl/https", 1337) is True


def test_should_execute_service_http_proxy():
    headers = HTTPHeaders()
    assert headers.should_execute("http-proxy", 1337) is True


def test_should_execute_service_https_alt():
    headers = HTTPHeaders()
    assert headers.should_execute("https-alt", 1337) is True


def test_should_execute_port_80():
    headers = HTTPHeaders()
    assert headers.should_execute("web-service", 80) is True


def test_should_execute_port_443():
    headers = HTTPHeaders()
    assert headers.should_execute("web-service", 443) is True


def test_should_execute_port_8008():
    headers = HTTPHeaders()
    assert headers.should_execute("web-service", 8008) is True


def test_should_execute_port_8080():
    headers = HTTPHeaders()
    assert headers.should_execute("web-service", 8080) is True


def test_should_execute_port_8443():
    headers = HTTPHeaders()
    assert headers.should_execute("web-service", 8443) is True


def test_should_not_execute():
    headers = HTTPHeaders()
    assert headers.should_execute("unknown-service", 1337) is False


def test_get_http():
    headers = HTTPHeaders()

    hostname = "httpforever.com"
    port = 80

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


def test_get_https():
    headers = HTTPHeaders()

    hostname = "www.google.com"
    port = 443

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


def test_get_non_standard():
    headers = HTTPHeaders()

    hostname = "www.facepunch.com"
    port = 8080

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)


def test_get_invalid_url():
    headers = HTTPHeaders()

    hostname = "kekekekekekeke.kek"
    port = 80

    headers.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][headers.loot_name] is not None
    assert isinstance(Loot.loot[hostname][port][headers.loot_name], dict)
