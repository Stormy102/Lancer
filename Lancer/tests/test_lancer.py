import lancer
import lancerargs
import config
import pytest
import io
import sys
import os
import tempfile


def test_setup_config_file():
    lancerargs.parse_arguments(["-T", "127.0.0.1"])
    lancer.setup()
    assert os.path.exists(config.nmap_cache())
    assert os.path.exists(config.gobuster_cache())
    assert os.path.exists(config.ftp_cache())


def test_setup_args_root():
    temp_dir = tempfile.TemporaryDirectory()
    lancerargs.parse_arguments(["-T", "127.0.0.1", "--cache-root", temp_dir.name])
    lancer.setup()
    assert os.path.exists(config.nmap_cache())
    assert os.path.exists(config.gobuster_cache())
    assert os.path.exists(config.ftp_cache())
    temp_dir.cleanup()


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
