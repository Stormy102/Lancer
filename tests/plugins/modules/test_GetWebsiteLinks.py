# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.GetWebsiteLinks import GetWebsiteLinks
from core import Loot, config

import pytest


@pytest.mark.module
def test_module_creation():
    links = GetWebsiteLinks()
    assert links is not None


@pytest.mark.module
def test_is_internal_url_same_tld():
    links = GetWebsiteLinks()
    assert links.is_internal_url("test.com", "example.test.com") is True


@pytest.mark.module
def test_is_internal_url_blank_domain():
    links = GetWebsiteLinks()
    assert links.is_internal_url("", "example.test.com") is True


@pytest.mark.module
def test_is_not_internal_url():
    links = GetWebsiteLinks()
    assert links.is_internal_url("example.com", "test.com") is False


@pytest.mark.module
def test_get_http():
    links = GetWebsiteLinks()

    hostname = "httpforever.com"
    port = 80

    links.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][links.loot_name] is not None
    assert len(Loot.loot[hostname][port][links.loot_name]["Internal"]) > 0
    assert len(Loot.loot[hostname][port][links.loot_name]["External"]) > 0


@pytest.mark.module
def test_get_https():
    links = GetWebsiteLinks()

    hostname = "www.google.com"
    port = 443

    links.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][links.loot_name] is not None
    assert len(Loot.loot[hostname][port][links.loot_name]["Internal"]) > 0
    assert len(Loot.loot[hostname][port][links.loot_name]["External"]) > 0


@pytest.mark.module
def test_get_non_standard():
    links = GetWebsiteLinks()

    hostname = "www.facepunch.com"
    port = 8080

    links.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][links.loot_name] is not None
    # Doesn't work due to Javascript not functioning, but the functionality
    # is tested in other tests (test_GetWebsiteLinks::test_get_https and
    # test_GetWebsiteLinks::test_get_http)
    assert not Loot.loot[hostname][port][links.loot_name]["Internal"]
    assert not Loot.loot[hostname][port][links.loot_name]["External"]


@pytest.mark.module
def test_get_invalid_url():
    links = GetWebsiteLinks()

    hostname = "kekekekekekeke.kek"
    port = 80

    links.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][links.loot_name] is not None
    assert not Loot.loot[hostname][port][links.loot_name]["Internal"]
    assert not Loot.loot[hostname][port][links.loot_name]["External"]

