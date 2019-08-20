import pytest

from lancer import *

def func(x):
    return x + 1


def test_closes_critical_program_not_installed():
    with pytest.raises(SystemExit):
        ProgramInstalled("programthatdoesntexist", True)

def test_non_critical_program_not_installed():
    assert ProgramInstalled("programthatdoesntexist", False) == False
