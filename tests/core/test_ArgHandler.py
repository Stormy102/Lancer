# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import ArgHandler, config

import pytest
import io
import sys


@pytest.mark.core
def test_parse_arguments():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_target() is not None


@pytest.mark.core
def test_create_parser():
    parser = ArgHandler.create_parser()
    assert parser is not None


@pytest.mark.core
def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments([])


@pytest.mark.core
def test_quits_with_version():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments(["--version"])
    sys.stdout = sys.__stdout__
    assert config.__version__ in captured_output.getvalue()


@pytest.mark.core
def test_quits_with_help():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments(["--help"])
    sys.stdout = sys.__stdout__
    assert "Lancer - system vulnerability scanner" in captured_output.getvalue()


@pytest.mark.core
def test_get_target():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_target() is not None


@pytest.mark.core
def test_get_target_none():
    ArgHandler.parse_arguments(["-TF", "targets.lan"])
    assert ArgHandler.get_target() is None


@pytest.mark.core
def test_get_target_file():
    ArgHandler.parse_arguments(["-TF", "targets.lan"])
    assert ArgHandler.get_target_file() is not None


@pytest.mark.core
def test_get_target_file_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_target_file() is None


@pytest.mark.core
def test_get_nmap_file():
    ArgHandler.parse_arguments(["-TN", "targets.lan"])
    assert ArgHandler.get_nmap_file() is not None


@pytest.mark.core
def test_get_nmap_file_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_nmap_file() is None


@pytest.mark.core
def test_get_verbose():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-v"])
    assert ArgHandler.get_verbose()


@pytest.mark.core
def test_get_verbose_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_verbose() is False


@pytest.mark.core
def test_get_very_verbose():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-vv"])
    assert ArgHandler.get_very_verbose()


@pytest.mark.core
def test_get_very_verbose_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-v"])
    assert ArgHandler.get_very_verbose() is False


@pytest.mark.core
def test_get_language_code():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-l", "de"])
    assert ArgHandler.get_language_code() == "de"


@pytest.mark.core
def test_get_language_code_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_language_code() == "en"


@pytest.mark.core
def test_get_clear_cache():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "--clear-cache"])
    assert ArgHandler.get_clear_cache()


@pytest.mark.core
def test_get_clear_cache_none():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert ArgHandler.get_clear_cache() is False
