# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import config
from core.reports.JSONReport import JSONReport

import pytest
import os


@pytest.mark.core
def test_create_instance():
    report = JSONReport()
    assert report is not None


@pytest.mark.core
def test_generate_report():
    report = JSONReport()

    data = {"Test": "Test", "Spam": "Spam"}

    report.generate_report(data)

    assert os.path.exists(os.path.join(config.get_report_folder(), report.filename))
