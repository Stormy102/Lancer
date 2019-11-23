from modules.new.SSLCertificateExtractor import SSLCertificateExtractor

import Loot


def test_parse_non_sni():
    cert_extract = SSLCertificateExtractor()

    hostname = "www.google.com"
    port = 443

    cert_extract.execute(hostname, port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None


def test_parse_sni():
    cert_extract = SSLCertificateExtractor()

    hostname = "www.facepunch.com"
    port = 443

    cert_extract.execute(hostname, port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is False


def test_expired_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "expired.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is True


def test_expired_cert():
    cert_extract = SSLCertificateExtractor()

    hostname = "self-signed.badssl.com"
    port = 443

    cert_extract.execute(hostname, port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name] is not None
    assert Loot.loot[hostname][port][cert_extract.loot_name]["Expired"] is False
