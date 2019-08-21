import pytest

from lancer import *
from utils import *


def test_closes_critical_program_not_installed():
    with pytest.raises(SystemExit):
        program_installed("program_that_doesnt_exist", True, False)
        assert True


def test_non_critical_program_not_installed():
    assert program_installed("program_that_doesnt_exist", False, False) is False


def test_setup():
    setup()
    assert os.path.exists("nmap")
    assert os.path.exists("gobuster")


def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        parse_arguments()


def test_signal_handler_quits():
    with pytest.raises(SystemExit):
        signal_handler(None, None)
