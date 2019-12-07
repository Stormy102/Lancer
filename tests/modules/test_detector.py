#  -*- coding: utf-8 -*-
#
#  """
#      Copyright (c) 2019 Lancer developers
#      See the file 'LICENCE' for copying permissions
#  """
#

"""from modules.legacy import detector

import io
import sys


def test_detect_os():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    detector.detect_os(["cpe:/o:microsoft:windows:10"])
    sys.stdout = sys.__stdout__
    assert "Microsoft Windows 10" in captured_output.getvalue()


def test_detect_apps():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    detector.detect_apps(["cpe:/a:apache:http_server:2.4.29"])
    sys.stdout = sys.__stdout__
    assert "Apache Http Server 2.4.29" in captured_output.getvalue()
"""