# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core import updater, config

import pytest


@pytest.mark.core
@pytest.mark.flaky(reruns=2)
def test_get_latest_version():
    latest_version, pre_release = updater.get_latest_version()
    assert latest_version


@pytest.mark.core
def test_check_if_update_available_newer_version():
    assert updater.check_if_update_available("9999999.0.0")


@pytest.mark.core
def test_check_if_update_available_same():
    current_version = config.__version__[0:config.__version__.index(" ")]
    assert updater.check_if_update_available(current_version) is False


@pytest.mark.core
def test_check_if_update_available_older_version():
    assert updater.check_if_update_available("0.0.1") is False
