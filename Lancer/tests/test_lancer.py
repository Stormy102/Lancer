from lancer import *
from utils import *

import lancerargs

import pytest
import platform
import io
import sys
import tempfile
import argparse


def test_closes_critical_program_not_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1', '-v'])
    with pytest.raises(SystemExit):
        program_installed("program_that_doesnt_exist", True)


def test_non_critical_program_not_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1'])
    assert program_installed("program_that_doesnt_exist", False) is False


def test_non_critical_program_installed():
    lancerargs.parse_arguments(['-T', '127.0.0.1'])
    assert program_installed("python", False) is True


def test_setup():
    setup()
    assert os.path.exists("nmap")
    assert os.path.exists("gobuster")
    assert os.path.exists("ftp")


def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        lancerargs.parse_arguments([])


def test_signal_handler_quits():
    with pytest.raises(SystemExit):
        signal_handler(None, None)


def test_is_not_virtual_terminal():
    if platform.system().lower() is not "windows":
        assert is_not_virtual_terminal() is False


def test_normal_message():
    out = normal_message()
    assert "[+]" in out


def test_warning_message():
    out = warning_message()
    assert "[*]" in out


def test_error_message():
    out = error_message()
    assert "[!]" in out


def test_version():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    version()
    sys.stdout = sys.__stdout__
    assert config.__version__ in captured_output.getvalue()


def test_line_break():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    line_break(1)
    sys.stdout = sys.__stdout__
    assert "\n" in captured_output.getvalue()


def test_get_valid_http_code():
    code = get_http_code(404)
    assert "Not Found" in code


def test_get_invalid_http_code():
    code = get_http_code(418)
    assert "Unknown" in code


def test_input_message(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "some_input")
    input_message("Input Test")

    sys.stdout = sys.__stdout__
    assert "[>]" in captured_output.getvalue()


def test_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "y")
    legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "\n" in captured_output.getvalue()


def test_reject_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "no lol")
    with pytest.raises(SystemExit):
        legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "not been accepted" in captured_output.getvalue()


def test_parse_down_nmap_scan():
    xml_output = '<hosts up="0" down="1" total="1"/>'
    file_descriptor, file_path = tempfile.mkstemp(suffix='.tmp')

    open_file = os.fdopen(file_descriptor, 'w')
    open_file.write(xml_output)
    open_file.close()

    captured_output = io.StringIO()
    sys.stdout = captured_output

    with pytest.raises(SystemExit):
        parse_nmap_scan(file_path)

    sys.stdout = sys.__stdout__
    os.unlink(file_path)
    assert "unreachable" in captured_output.getvalue()


def test_print_header():
    captured_output = io.StringIO()
    sys.stdout = captured_output

    print_header()

    sys.stdout = sys.__stdout__
    assert "`.--:::::::::::::::::---." in captured_output.getvalue()


def test_create_parser():
    parser = lancerargs.create_parser()
    assert parser is not None

