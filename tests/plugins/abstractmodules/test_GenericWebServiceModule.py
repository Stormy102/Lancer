# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import config

import pytest


def create_module(required: bool = False) -> GenericWebServiceModule:
    return GenericWebServiceModule(name="Test",
                                   description="Test",
                                   loot_name="Test",
                                   intrusion_level=3,
                                   critical=required)


@pytest.mark.module
def test_module_creation():
    module = create_module()
    assert module is not None


@pytest.mark.module
def test_get_url_http():
    module = create_module()
    url = module.get_url("127.0.0.1", 80)
    assert "http://" in url
    assert ":80" not in url


@pytest.mark.module
def test_get_url_https():
    module = create_module()
    url = module.get_url("127.0.0.1", 443)
    assert "https://" in url
    assert ":443" not in url


@pytest.mark.module
def test_get_url_http_alt():
    module = create_module()
    url = module.get_url("127.0.0.1", 8080)
    assert "http://" in url
    assert ":8080" in url


@pytest.mark.module
def test_get_url_https_alt():
    module = create_module()
    url = module.get_url("127.0.0.1", 8443)
    assert "https://" in url
    assert ":8443" in url


@pytest.mark.module
def test_should_execute_service_http():
    module = create_module()
    assert module.should_execute("http", 1337)


@pytest.mark.module
def test_should_execute_service_https():
    module = create_module()
    assert module.should_execute("ssl/https", 1337)


@pytest.mark.module
def test_should_execute_service_http_proxy():
    module = create_module()
    assert module.should_execute("http-proxy", 1337)


@pytest.mark.module
def test_should_execute_service_https_alt():
    module = create_module()
    assert module.should_execute("https-alt", 1337)


@pytest.mark.module
def test_should_execute_port_80():
    module = create_module()
    assert module.should_execute("web-service", 80)


@pytest.mark.module
def test_should_execute_port_443():
    module = create_module()
    assert module.should_execute("web-service", 443)


@pytest.mark.module
def test_should_execute_port_8008():
    module = create_module()
    assert module.should_execute("web-service", 8008)


@pytest.mark.module
def test_should_execute_port_8080():
    module = create_module()
    assert module.should_execute("web-service", 8080)


@pytest.mark.module
def test_should_execute_port_8443():
    module = create_module()
    assert module.should_execute("web-service", 8443)


@pytest.mark.module
def test_disabled_config():
    module = create_module()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("http", 80)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_not_execute():
    module = create_module()
    assert module.should_execute("mysql", 3306) is False
