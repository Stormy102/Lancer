# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.ModuleExecuteState import ModuleExecuteState
from plugins.abstractmodules.BaseModule import BaseModule
from core import Loot, config, ArgHandler

import pytest


def create_module(required: bool = False) -> BaseModule:
    return BaseModule(name="Test",
                      description="Test",
                      loot_name="Test",
                      intrusion_level=3,
                      critical=required)


@pytest.mark.module
def test_module_creation():
    module = create_module()
    assert module is not None


@pytest.mark.module
def test_disabled_config():
    module = create_module()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("", 0)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_execute():
    module = create_module()

    assert module.should_execute("127.0.0.1", 0) is True


@pytest.mark.module
def test_create_loot():
    module = create_module()

    Loot.reset()

    ip = "127.0.0.1"
    port = 0

    module.create_loot_space(ip, port)

    port = str(0)

    assert Loot.loot[ip] is not None
    assert Loot.loot[ip][port] is not None
    assert Loot.loot[ip][port][module.loot_name] is not None


@pytest.mark.module
def test_execute():
    module = create_module(False)

    module.execute("127.0.0.1", 0)


@pytest.mark.module
def test_can_execute_module():
    module = create_module(False)
    ArgHandler.parse_arguments(["-T", "::1"])

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.CanExecute


@pytest.mark.module
def test_cannot_execute_module_intrusiveness_level():
    module = create_module(False)
    module.intrusion_level = 5
    ArgHandler.parse_arguments(["-T", "::1"])

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.SkipExecute


@pytest.mark.module
def test_cannot_execute_module():
    module = create_module(False)
    module.required_programs = ["fake_lancer_requirement"]

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.SkipExecute


@pytest.mark.module
def test_cannot_execute_critical_module():
    module = create_module(True)
    module.required_programs = ["fake_lancer_requirement"]

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.CannotExecute
