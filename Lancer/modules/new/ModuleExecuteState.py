from enum import Enum, auto


class ModuleExecuteState(Enum):
    CanExecute = auto()
    CannotExecute = auto()
    SkipExecute = auto()
