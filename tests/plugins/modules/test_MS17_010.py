# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.MS17_010 import MS17_010

import pytest


@pytest.mark.module
def test_should_execute_service():
    module = MS17_010()
    assert module.should_execute("microsoft-ds", 4455)


@pytest.mark.module
def test_should_execute_port():
    module = MS17_010()
    assert module.should_execute("SMB", 445)


@pytest.mark.module
def test_should_not_execute():
    module = MS17_010()
    assert module.should_execute("SMB", 4455) is False