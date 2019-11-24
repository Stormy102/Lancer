#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.new.SSLCertificateExtractor import SSLCertificateExtractor

import Loot


def test_module_creation():
    cert_extract = SSLCertificateExtractor()
    assert cert_extract is not None


def test_should_run_service():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("ssl/https", 443)

    assert result is True


def test_should_run_port():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("ssl/https", 4433)

    assert result is True


def test_should_not_run():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("http", 80)

    assert result is False


def test_parse_non_sni():
    cert_extract = SSLCertificateExtractor()

    hostname = "www.google.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None


def test_parse_sni():
    cert_extract = SSLCertificateExtractor()

    hostname = "www.facepunch.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is False


def test_expired_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "expired.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is True


def test_expired_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "self-signed.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is False
