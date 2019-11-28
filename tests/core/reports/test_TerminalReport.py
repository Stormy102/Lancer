# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.reports.TerminalReport import TerminalReport

import pytest
import io
import sys


@pytest.mark.core
def test_create_instance():
    report = TerminalReport()
    assert report is not None


@pytest.mark.core
def test_generate_report():
    report = TerminalReport()

    service = {"options": ["GET", "POST", "OPTIONS"]}

    geo_service = {"host": "example.com", "ip": "127.0.0.1"}

    ports = {"21": service, "geo": geo_service}

    root = {"example.com": ports}

    captured_output = io.StringIO()
    sys.stdout = captured_output
    report.generate_report(root)
    sys.stdout = sys.__stdout__

    out = captured_output.getvalue()

    assert "Target: example.com" in out
    assert "Port: 21" in out
    assert " geo" in out
    assert " options:" in out
    assert "- GET" in out
    assert "host: example.com" in out
    assert "ip: 127.0.0.1" in out
