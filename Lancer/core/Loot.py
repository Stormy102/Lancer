# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

import json

loot = {}


def reset():
    global loot
    loot = {}


def to_json():
    return json.dumps(loot, sort_keys=True, indent=4)