# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import config
from core.reports.Report import Report

import pytest
import os


@pytest.mark.core
def test_create_instance():
    report = Report()
    assert report is not None


@pytest.mark.core
def test_generate_report():
    report = Report()

    data = {"Test": "Test", "Spam": "Spam"}

    assert report.generate_report(data) is None
