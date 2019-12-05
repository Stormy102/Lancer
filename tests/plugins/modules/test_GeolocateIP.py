# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.GeolocateIP import GeolocateIP
from core import Loot, config

import pytest


@pytest.mark.module
def test_module_creation():
    geolocate_ip = GeolocateIP()
    assert geolocate_ip is not None


@pytest.mark.module
def test_should_execute():
    module = GeolocateIP()
    assert module.should_execute("", 0)


@pytest.mark.module
def test_should_not_execute():
    module = GeolocateIP()
    assert not module.should_execute("", 21)


@pytest.mark.module
def test_create_loot_space():
    geolocate_ip = GeolocateIP()

    ip = "1.1.1.1"

    geolocate_ip.create_loot_space(ip, 0)

    assert Loot.loot[ip] is not None
    assert Loot.loot[ip][geolocate_ip.loot_name] is not None


@pytest.mark.module
def test_get_valid_domain_name():
    geolocate_ip = GeolocateIP()

    hostname = "www.facepunch.com"

    geolocate_ip.execute(hostname, 0)

    assert "Cloudflare" in Loot.loot[hostname][geolocate_ip.loot_name]["isp"]


@pytest.mark.module
def test_get_valid_ip():
    geolocate_ip = GeolocateIP()

    # Cloudflare IP
    hostname = "104.27.155.47"

    geolocate_ip.execute(hostname, 0)

    assert "Cloudflare" in Loot.loot[hostname][geolocate_ip.loot_name]["isp"]


@pytest.mark.module
def test_get_invalid_ip():
    geolocate_ip = GeolocateIP()

    hostname = "127.0.0.1"

    geolocate_ip.execute(hostname, 0)

    assert not Loot.loot[hostname][geolocate_ip.loot_name]["isp"]
