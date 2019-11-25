# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.SMBClient import SMBClient


def test_module_creation():
    smb = SMBClient()
    assert smb is not None


def test_should_run_service():
    smb = SMBClient()

    result = smb.should_execute("microsoft-ds", 4455)

    assert result is True


def test_should_run_port():
    smb = SMBClient()

    result = smb.should_execute("ms-ds", 445)

    assert result is True


def test_should_not_run():
    smb = SMBClient()

    result = smb.should_execute("msrpc", 139)

    assert result is False
