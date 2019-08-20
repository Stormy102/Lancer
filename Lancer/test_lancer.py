import pytest
import os

from lancer import *

def test_closes_critical_program_not_installed():
    with pytest.raises(SystemExit):
        ProgramInstalled("programthatdoesntexist", True)
        assert True

def test_non_critical_program_not_installed():
    assert ProgramInstalled("programthatdoesntexist", False) == False

def test_setup():
    Setup()
    assert os.path.exists("nmap")

def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        ParseArguments()
        assert True

def test_signal_handler_quits():
    with pytest.raises(SystemExit):
        SignalHandler(None, None)
        assert True
