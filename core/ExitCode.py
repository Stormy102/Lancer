# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from enum import IntEnum


class ExitCode(IntEnum):
    OK = 0
    NotImplemented = -1
    CriticalDependencyNotInstalled = 1
    EntryPointModulesNotLoaded = 2
    PluginDirectoryMissing = 3
    EntryPointModuleDirectoryMissing = 4
    ModuleDirectoryMissing = 5
    UnknownError = 255

