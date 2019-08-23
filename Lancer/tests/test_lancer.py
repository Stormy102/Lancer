import lancer
import pytest
import io
import sys
import os


def test_setup():
    lancer.setup()
    assert os.path.exists("nmap")
    assert os.path.exists("gobuster")
    assert os.path.exists("ftp")


def test_signal_handler_quits():
    with pytest.raises(SystemExit):
        lancer.signal_handler(None, None)


def test_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "y")
    lancer.legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "\n" in captured_output.getvalue()


def test_reject_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "no lol")
    with pytest.raises(SystemExit):
        lancer.legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "not been accepted" in captured_output.getvalue()
