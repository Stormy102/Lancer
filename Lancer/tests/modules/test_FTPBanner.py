#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.FTPBanner import FTPBanner

import Loot
import warnings


def test_module_creation():
    banner = FTPBanner()
    assert banner is not None


def test_should_run_service():
    banner = FTPBanner()

    result = banner.should_execute("ftp", 2121)

    assert result is True


def test_should_run_port():
    banner = FTPBanner()

    result = banner.should_execute("ftpd", 21)

    assert result is True


def test_should_not_run():
    banner = FTPBanner()

    result = banner.should_execute("ssh", 22)

    assert result is False


def test_get_banner():
    banner = FTPBanner()

    hostname = "speedtest.tele2.net"
    port = 21

    try:
        banner.execute(hostname, port)

        port = str(port)

        assert Loot.loot[hostname] is not None
        assert Loot.loot[hostname][port] is not None
        assert Loot.loot[hostname][port][banner.loot_name] is not None

        if "Banner" not in Loot.loot[hostname][port][banner.loot_name]:
            warnings.warn("Banner not present")
            raise AssertionError()
        assert Loot.loot[hostname][port][banner.loot_name]['Banner'] is not None
    except AssertionError:
        warnings.warn("Unable to connect to speedtest.tele2.net")


def test_get_banner_unreachable():
    banner = FTPBanner()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2121

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
    assert "Banner" not in Loot.loot[hostname][port][banner.loot_name]


def test_get_banner_invalid():
    banner = FTPBanner()
    Loot.reset()

    hostname = "ftp.invali.de"
    port = 21

    banner.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][banner.loot_name] is not None
