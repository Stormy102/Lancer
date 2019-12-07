# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

import json

loot = {}


def reset():
    """
    Resets the loot to a new dictionary
    """
    global loot
    loot = {}
