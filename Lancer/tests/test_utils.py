import utils
import lancerargs
import config

import pytest
import io
import platform
import sys


def test_closes_critical_program_not_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1', '-v'])
    with pytest.raises(SystemExit):
        utils.program_installed("program_that_doesnt_exist", True)


def test_non_critical_program_not_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1', '-v'])
    assert utils.program_installed("program_that_doesnt_exist", False) is False


def test_non_critical_program_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1', '-v'])
    assert utils.program_installed("python", False) is True


def test_is_not_virtual_terminal():
    if platform.system().lower() is not "windows":
        assert utils.is_not_virtual_terminal() is False


def test_normal_message():
    out = utils.normal_message()
    assert "[+]" in out


def test_warning_message():
    out = utils.warning_message()
    assert "[*]" in out


def test_error_message():
    out = utils.error_message()
    assert "[!]" in out


def test_version():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    utils.version()
    sys.stdout = sys.__stdout__
    assert config.__version__ in captured_output.getvalue()


def test_line_break():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    utils.line_break(1)
    sys.stdout = sys.__stdout__
    assert "\n" in captured_output.getvalue()


def test_get_valid_http_code():
    code = utils.get_http_code(404)
    assert "Not Found" in code


def test_get_invalid_http_code():
    # It is tragic that "I'm a teapot" isn't recognised by Python's HTTP client
    code = utils.get_http_code(418)
    assert "Unknown" in code


def test_input_message(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "some_input")
    utils.input_message("Input Test")

    sys.stdout = sys.__stdout__
    assert "[>]" in captured_output.getvalue()


def test_print_header():
    captured_output = io.StringIO()
    sys.stdout = captured_output

    utils.print_header()

    sys.stdout = sys.__stdout__
    # Just check the top line of the header
    assert "`.--:::::::::::::::::---." in captured_output.getvalue()
