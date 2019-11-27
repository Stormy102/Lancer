import lancer
from core import ArgHandler, config
import pytest
import io
import sys
import os
import tempfile


@pytest.mark.core
def test_setup_config_file():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    lancer.setup()
    assert os.path.exists(config.nmap_cache())
    assert os.path.exists("nmap") # Default cache path in config file
    assert os.path.exists(config.gobuster_cache())
    assert os.path.exists("gobuster")  # Default cache path in config file
    assert os.path.exists(config.ftp_cache())
    assert os.path.exists("ftp")  # Default cache path in config file


@pytest.mark.core
def test_setup_args_root():
    temp_dir = tempfile.TemporaryDirectory()
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "--cache-root", temp_dir.name])
    lancer.setup()
    assert os.path.exists(config.nmap_cache())
    assert os.path.exists(config.gobuster_cache())
    assert os.path.exists(config.ftp_cache())
    assert os.path.exists(config.nikto_cache())
    temp_dir.cleanup()



@pytest.mark.core
def test_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "y")
    lancer.legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "\n" in captured_output.getvalue()


@pytest.mark.core
def test_reject_legal_disclaimer(monkeypatch):
    captured_output = io.StringIO()
    sys.stdout = captured_output

    monkeypatch.setattr('builtins.input', lambda: "no lol")
    with pytest.raises(SystemExit):
        lancer.legal_disclaimer()

    sys.stdout = sys.__stdout__
    assert "not been accepted" in captured_output.getvalue()
