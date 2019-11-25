# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.ModuleExecuteState import ModuleExecuteState
from modules.BaseModule import BaseModule

from core import Loot


def create_module(required: bool = False) -> BaseModule:
    return BaseModule(name="Test",
                      description="Test",
                      loot_name="Test",
                      multithreaded=False,
                      critical=required,
                      intrusive=False)


def test_module_creation():
    module = create_module()
    assert module is not None


def test_should_execute():
    module = create_module()

    assert module.should_execute("127.0.0.1", 0) is True


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


def test_execute():
    module = create_module(False)

    module.execute("127.0.0.1", 0)


def test_can_execute_module():
    module = create_module(False)

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.CanExecute


def test_cannot_execute_module():
    module = create_module(False)
    module.required_programs = ["fake_lancer_requirement"]

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.SkipExecute


def test_cannot_execute_critical_module():
    module = create_module(True)
    module.required_programs = ["fake_lancer_requirement"]

    ret = module.can_execute_module()

    assert ret is ModuleExecuteState.CannotExecute
