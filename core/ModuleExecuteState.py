# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from enum import Enum


class ModuleExecuteState(Enum):
    """
    The states which a module can be in
    - Can Execute - the module has all the dependencies met and can be executed without issue
    - Cannot Execute - the module is missing dependencies and cannot be executed
    - Skip Execute - the module is missing dependencies, but is non-critical and can be skipped
    """
    CanExecute = 1
    CannotExecute = 2
    SkipExecute = 4
