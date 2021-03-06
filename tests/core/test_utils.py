from core import ArgHandler, config, utils

import pytest
import io
import sys


@pytest.mark.core
def test_signal_handler_quits():
    with pytest.raises(SystemExit):
        utils.signal_handler(0, None)


@pytest.mark.core
def test_normal_message():
    out = utils.normal_message()
    assert "[+]" in out


@pytest.mark.core
def test_warning_message():
    out = utils.warning_message()
    assert "[*]" in out


@pytest.mark.core
def test_error_message():
    out = utils.error_message()
    assert "[!]" in out


@pytest.mark.core
def test_version():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    utils.display_header()
    sys.stdout = sys.__stdout__
    assert config.__version__ in captured_output.getvalue()


@pytest.mark.core
def test_python_version():
    try:
        utils.python_version()
    except SystemExit:
        pytest.fail()


@pytest.mark.core
def test_get_valid_http_code():
    code = utils.get_http_code(404)
    assert "Not Found" in code


@pytest.mark.core
def test_get_invalid_http_code():
    # It is tragic that "I'm a teapot" isn't recognised by Python's HTTP client
    code = utils.get_http_code(418)
    assert "Unknown" in code


@pytest.mark.core
def test_input_message(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "some_input")
    utils.input_message("Input Test")

    sys.stdout = sys.__stdout__
    assert "[>]" in captured_output.getvalue()


@pytest.mark.core
def test_print_header():
    captured_output = io.StringIO()
    sys.stdout = captured_output

    utils.print_header()

    sys.stdout = sys.__stdout__
    # Just check the top line of the header
    assert "`.--:::::::::::::::::---." in captured_output.getvalue()


@pytest.mark.core
def test_style_bold():
    assert utils.get_text_style("bold") is "1"


@pytest.mark.core
def test_style_underlined():
    assert utils.get_text_style("underline") is "2"


@pytest.mark.core
def test_style_negative1():
    assert utils.get_text_style("negative1") is "3"


@pytest.mark.core
def test_style_negative2():
    assert utils.get_text_style("negative2") is "5"


@pytest.mark.core
def test_style_invalid():
    assert utils.get_text_style("invalid") is "0"


@pytest.mark.core
def test_foreground_red():
    assert utils.get_foreground_color("red") is "31"


@pytest.mark.core
def test_foreground_green():
    assert utils.get_foreground_color("green") is "32"


@pytest.mark.core
def test_foreground_yellow():
    assert utils.get_foreground_color("yellow") is "33"


@pytest.mark.core
def test_foreground_blue():
    assert utils.get_foreground_color("blue") is "34"


@pytest.mark.core
def test_foreground_purple():
    assert utils.get_foreground_color("purple") is "35"


@pytest.mark.core
def test_foreground_cyan():
    assert utils.get_foreground_color("cyan") is "36"


@pytest.mark.core
def test_foreground_black():
    assert utils.get_foreground_color("black") is "30"


@pytest.mark.core
def test_foreground_invalid():
    assert utils.get_foreground_color("invalid") is "37"


@pytest.mark.core
def test_background_red():
    assert utils.get_background_color("red") is "41"


@pytest.mark.core
def test_background_green():
    assert utils.get_background_color("green") is "42"


@pytest.mark.core
def test_background_yellow():
    assert utils.get_background_color("yellow") is "43"


@pytest.mark.core
def test_background_blue():
    assert utils.get_background_color("blue") is "44"


@pytest.mark.core
def test_background_purple():
    assert utils.get_background_color("purple") is "45"


@pytest.mark.core
def test_background_cyan():
    assert utils.get_background_color("cyan") is "46"


@pytest.mark.core
def test_background_white():
    assert utils.get_background_color("white") is "47"


@pytest.mark.core
def test_background_invalid():
    assert utils.get_background_color("invalid") is "40"


@pytest.mark.core
def test_color_background():
    assert "46" in utils.color("Lorem ipsum dolar sit amet", "White", "Cyan")


@pytest.mark.core
def test_color_style():
    assert "37" in utils.color("Lorem ipsum dolar sit amet", style="bold")


@pytest.mark.core
def test_is_valid_target_valid():
    assert utils.is_valid_target("google.co.uk") is True


@pytest.mark.core
def test_is_valid_target_invalid():
    assert utils.is_valid_target("256.128.64.32") is False
