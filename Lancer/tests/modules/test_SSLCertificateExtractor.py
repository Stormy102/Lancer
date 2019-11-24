#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from modules.SSLCertificateExtractor import SSLCertificateExtractor

from core import Loot


def test_module_creation():
    cert_extract = SSLCertificateExtractor()
    assert cert_extract is not None


def test_should_run_service_sslhttps():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("ssl/https", 4433)

    assert result is True


def test_should_run_service_https():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("https", 4433)

    assert result is True


def test_should_run_port():
    cert_extract = SSLCertificateExtractor()

    result = cert_extract.should_execute("http", 443)

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

    assert Loot.loot[hostname][port][cert_extract.loot_name]["Common Name"] == "www.google.com"


def test_parse_sni():
    cert_extract = SSLCertificateExtractor()

    hostname = "www.facepunch.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert "cloudflaressl.com" in Loot.loot[hostname][port][cert_extract.loot_name]["Common Name"]


def test_expired_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "expired.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is True


def test_no_common_name_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "no-common-name.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][cert_extract.loot_name]["Common Name"] is None


def test_self_signed_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "self-signed.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert "badssl.com" in Loot.loot[hostname][port][cert_extract.loot_name]["Common Name"]


def test_no_subject_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "no-subject.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname][port][cert_extract.loot_name]["Common Name"] is None
