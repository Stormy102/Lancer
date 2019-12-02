# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.ModuleExecuteState import ModuleExecuteState
from plugins.abstractmodules.GenericWebServiceModule import GenericWebServiceModule
from core import Loot, config

import pytest


def create_module(required: bool = False) -> GenericWebServiceModule:
    return GenericWebServiceModule(name="Test",
                                   description="Test",
                                   loot_name="Test",
                                   multithreaded=False,
                                   critical=required,
                                   intrusive=False)


@pytest.mark.module
def test_module_creation():
    module = create_module()
    assert module is not None


@pytest.mark.module
def test_should_execute_service_http():
    module = create_module()
    assert module.should_execute("http", 1337) is True


@pytest.mark.module
def test_should_execute_service_https():
    module = create_module()
    assert module.should_execute("ssl/https", 1337) is True


@pytest.mark.module
def test_should_execute_service_http_proxy():
    module = create_module()
    assert module.should_execute("http-proxy", 1337) is True


@pytest.mark.module
def test_should_execute_service_https_alt():
    module = create_module()
    assert module.should_execute("https-alt", 1337) is True


@pytest.mark.module
def test_should_execute_port_80():
    module = create_module()
    assert module.should_execute("web-service", 80) is True


@pytest.mark.module
def test_should_execute_port_443():
    module = create_module()
    assert module.should_execute("web-service", 443) is True


@pytest.mark.module
def test_should_execute_port_8008():
    module = create_module()
    assert module.should_execute("web-service", 8008) is True


@pytest.mark.module
def test_should_execute_port_8080():
    module = create_module()
    assert module.should_execute("web-service", 8080) is True


@pytest.mark.module
def test_should_execute_port_8443():
    module = create_module()
    assert module.should_execute("web-service", 8443) is True
