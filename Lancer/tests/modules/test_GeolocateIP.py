#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.GeolocateIP import GeolocateIP

import Loot


def test_module_creation():
    geolocate_ip = GeolocateIP()
    assert geolocate_ip is not None


def test_should_run():
    geolocate_ip = GeolocateIP()

    result = geolocate_ip.should_execute("", 0)

    assert result is True


def test_get_valid_domain_name():
    geolocate_ip = GeolocateIP()

    hostname = "www.facepunch.com"

    geolocate_ip.execute(hostname, 0)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][geolocate_ip.loot_name] is not None
    assert "Cloudflare" in Loot.loot[hostname][geolocate_ip.loot_name]["isp"]


def test_get_valid_ip():
    geolocate_ip = GeolocateIP()

    # Cloudflare IP
    hostname = "104.27.155.47"

    geolocate_ip.execute(hostname, 0)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][geolocate_ip.loot_name] is not None
    assert "Cloudflare" in Loot.loot[hostname][geolocate_ip.loot_name]["isp"]


def test_get_invalid_ip():
    geolocate_ip = GeolocateIP()

    hostname = "127.0.0.1"

    geolocate_ip.execute(hostname, 0)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][geolocate_ip.loot_name] is not None
    assert not Loot.loot[hostname][geolocate_ip.loot_name]["isp"]
