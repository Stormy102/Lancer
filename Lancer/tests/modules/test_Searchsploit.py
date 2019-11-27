# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.Searchsploit import Searchsploit

import pytest


@pytest.mark.module
def test_module_creation():
    exploit_db = Searchsploit()
    assert exploit_db is not None


@pytest.mark.module
def test_should_run_service():
    exploit_db = Searchsploit()

    assert exploit_db.should_execute("", 0) is True
