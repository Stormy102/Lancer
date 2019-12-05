# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.Searchsploit import Searchsploit
from core import config

import pytest


@pytest.mark.module
def test_module_creation():
    exploit_db = Searchsploit()
    assert exploit_db is not None
