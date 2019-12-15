# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.abstractmodules.SSHModule import SSHModule
from core import config

import pytest


def create_module(required: bool = False) -> SSHModule:
    return SSHModule(name="Test",
                     description="Test",
                     loot_name="Test",
                     intrusion_level=3,
                     critical=required)


@pytest.mark.module
def test_module_creation():
    module = create_module()
    assert module is not None


@pytest.mark.module
def test_should_execute_service():
    module = create_module()
    assert module.should_execute("ssh", 2222)


@pytest.mark.module
def test_should_execute_port():
    module = create_module()
    assert module.should_execute("win-ssh", 22)


@pytest.mark.module
def test_disabled_config():
    module = create_module()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("ssh", 22)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_not_execute():
    module = create_module()
    assert module.should_execute("http", 8080) is False
