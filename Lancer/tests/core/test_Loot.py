# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import Loot


def test_loot_json():
    Loot.reset()

    Loot.loot["Test"] = "Testing"

    assert Loot.to_json()[0] == "{"


def test_loot_reset():
    Loot.loot["Test"] = "Testing"

    assert len(Loot.loot.keys()) > 0

    Loot.reset()

    assert len(Loot.loot.keys()) == 0
