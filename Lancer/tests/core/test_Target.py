# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from core.Target import Target

import time


def test_target_get_hostname():
    target = Target("example.com", "127.0.0.1")
    assert target.get_address() is "example.com"


def test_target_get_ip():
    target = Target(None, "127.0.0.1")
    assert target.get_address() is "127.0.0.1"


def test_target_time_elapsed_ip():
    target = Target(None, "127.0.0.1")
    time.sleep(0.1)
    target.stop_timer()
    assert target.elapsed_time is not target.start_time
    assert target.finish_time > target.start_time
    assert target.elapsed_time > 0
    assert target.time_taken is not None


def test_target_time_elapsed_hostname():
    target = Target("example.com", "127.0.0.1")
    time.sleep(0.1)
    target.stop_timer()
    assert target.elapsed_time is not target.start_time
    assert target.finish_time > target.start_time
    assert target.elapsed_time > 0
    assert target.time_taken is not None
