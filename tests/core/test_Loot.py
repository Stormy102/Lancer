# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import Loot

import pytest


@pytest.mark.core
def test_loot_reset():
    Loot.loot["Test"] = "Testing"

    assert len(Loot.loot.keys()) > 0

    Loot.reset()

    assert len(Loot.loot.keys()) == 0
