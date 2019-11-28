# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.SMBClient import SMBClient
from core import config

import pytest


@pytest.mark.module
def test_module_creation():
    smb = SMBClient()
    assert smb is not None


@pytest.mark.module
def test_disabled_config():
    module = SMBClient()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "False")

    result = module.should_execute("ftp", 2121)

    config.config.set(module.name, "enabled", "True")

    assert result is False


@pytest.mark.module
def test_should_run_service():
    smb = SMBClient()

    result = smb.should_execute("microsoft-ds", 4455)

    assert result is True


@pytest.mark.module
def test_should_run_port():
    smb = SMBClient()

    result = smb.should_execute("ms-ds", 445)

    assert result is True


@pytest.mark.module
def test_should_not_run():
    smb = SMBClient()

    result = smb.should_execute("msrpc", 139)

    assert result is False
