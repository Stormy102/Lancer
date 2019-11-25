# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""
from core.InvalidTarget import InvalidTarget
from core.Target import Target

import time
import pytest


def test_target_creation_valid_ip():
    target = Target("127.0.0.1")
    assert target is not None


def test_target_creation_valid_hostname():
    target = Target("www.google.com")
    assert target is not None


def test_target_creation_invalid_ip():
    with pytest.raises(InvalidTarget):
        Target("256.128.64.32")


def test_target_creation_invalid_hostname():
    with pytest.raises(InvalidTarget):
        Target("invalid.hostname")


def test_target_time_elapsed():
    target = Target("127.0.0.1")
    time.sleep(0.01)
    target.stop_timer()
    assert target.elapsed_time is not target.start_time
    assert target.finish_time > target.start_time
    assert target.elapsed_time > 0
    assert target.time_taken is not None
