from enum import Enum


class ModuleExecuteState(Enum):
    CanExecute = 1
    CannotExecute = 2
    SkipExecute = 3
