# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from enum import Enum


class ModuleExecuteState(Enum):
    CanExecute = 1
    CannotExecute = 2
    SkipExecute = 4
