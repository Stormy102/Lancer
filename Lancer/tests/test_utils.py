import utils
import lancerargs
import config

import pytest
import io
import platform
import sys

# TODO: Test text foreground/background colouring tests and styles


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


def test_style_bold():
    assert utils.get_text_style("bold") is "1"


def test_style_underlined():
    assert utils.get_text_style("underline") is "2"


def test_style_negative1():
    assert utils.get_text_style("negative1") is "3"


def test_style_negative2():
    assert utils.get_text_style("negative2") is "5"


def test_style_invalid():
    assert utils.get_text_style("invalid") is "0"


def test_foreground_red():
    assert utils.get_foreground_color("red") is "31"


def test_foreground_green():
    assert utils.get_foreground_color("green") is "32"


def test_foreground_yellow():
    assert utils.get_foreground_color("yellow") is "33"


def test_foreground_blue():
    assert utils.get_foreground_color("blue") is "34"


def test_foreground_purple():
    assert utils.get_foreground_color("purple") is "35"


def test_foreground_cyan():
    assert utils.get_foreground_color("cyan") is "36"


def test_foreground_black():
    assert utils.get_foreground_color("black") is "30"


def test_foreground_invalid():
    assert utils.get_foreground_color("invalid") is "37"


def test_background_red():
    assert utils.get_background_color("red") is "41"


def test_background_green():
    assert utils.get_background_color("green") is "42"


def test_background_yellow():
    assert utils.get_background_color("yellow") is "43"


def test_background_blue():
    assert utils.get_background_color("blue") is "44"


def test_background_purple():
    assert utils.get_background_color("purple") is "45"


def test_background_cyan():
    assert utils.get_background_color("cyan") is "46"


def test_background_white():
    assert utils.get_background_color("white") is "47"


def test_background_invalid():
    assert utils.get_background_color("invalid") is "40"


def test_color_background():
    assert "46" in utils.color("Lorem ipsum dolar sit amet", "White", "Cyan")
