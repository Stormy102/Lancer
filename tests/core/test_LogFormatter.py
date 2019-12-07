# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.LogFormatter import LogFormatter
from core import utils, ArgHandler

import pytest
import logging


@pytest.mark.core
def test_normal_message():
    formatter = LogFormatter()
    record = logging.LogRecord(name="TEST", level=logging.INFO, pathname=None, lineno=1, msg="Testing", args=None,
                               exc_info=None)
    assert "[TEST]" in formatter.format(record)
    assert "Testing" in formatter.format(record)
    assert utils.normal_message() in formatter.format(record)


@pytest.mark.core
def test_warning_message_non_verbose():
    formatter = LogFormatter()
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    record = logging.LogRecord(name="TEST", level=logging.WARNING, pathname=None, lineno=1, msg="Testing", args=None,
                               exc_info=None)
    assert "[TEST]" not in formatter.format(record)
    assert "Testing" in formatter.format(record)
    assert utils.warning_message() in formatter.format(record)


@pytest.mark.core
def test_warning_message_verbose():
    formatter = LogFormatter()
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-v"])
    record = logging.LogRecord(name="TEST", level=logging.WARNING, pathname=None, lineno=1, msg="Testing", args=None,
                               exc_info=None)
    assert "[TEST]" in formatter.format(record)
    assert "Testing" in formatter.format(record)
    assert utils.warning_message() in formatter.format(record)


@pytest.mark.core
def test_exception_message():
    formatter = LogFormatter()
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-v"])
    record = logging.LogRecord(name="TEST", level=logging.ERROR, pathname=None, lineno=1, msg="Testing", args=None,
                               exc_info=None)
    assert "[TEST]" in formatter.format(record)
    assert "Testing" in formatter.format(record)
    assert utils.error_message() in formatter.format(record)
