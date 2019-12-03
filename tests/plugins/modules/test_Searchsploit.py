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


@pytest.mark.module
def test_disabled_config():
    module = Searchsploit()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("ftp", 21)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_run_service():
    exploit_db = Searchsploit()

    assert exploit_db.should_execute("", 0) is True
