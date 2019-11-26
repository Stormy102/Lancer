# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import ArgHandler, config
import pytest
import io
import sys


def test_parse_arguments():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert config.args.target is not None


def test_create_parser():
    parser = ArgHandler.create_parser()
    assert parser is not None


def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments([])


def test_quits_with_version():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments(["--version"])
    sys.stdout = sys.__stdout__
    assert config.__version__ in captured_output.getvalue()
