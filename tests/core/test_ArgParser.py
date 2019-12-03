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
