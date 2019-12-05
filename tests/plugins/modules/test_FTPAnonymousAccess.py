# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.FTPAnonymousAccess import FTPAnonymousAccess
from core import config, Loot

import pytest
import ftplib
import warnings
import os


@pytest.mark.module
def test_module_creation():
    module = FTPAnonymousAccess()
    assert module is not None


@pytest.mark.module
def test_disabled_config():
    module = FTPAnonymousAccess()

    if module.name not in config.config:
        config.config.add_section(module.name)
    config.config.set(module.name, "enabled", "no")

    result = module.should_execute("ftp", 21)

    config.config.set(module.name, "enabled", "yes")

    assert result is False


@pytest.mark.module
def test_should_run_service():
    module = FTPAnonymousAccess()
    assert module.should_execute("ftp", 2121)


@pytest.mark.module
def test_should_run_port():
    module = FTPAnonymousAccess()
    assert module.should_execute("ftpd", 21)


@pytest.mark.module
def test_should_not_run():
    module = FTPAnonymousAccess()
    assert module.should_execute("ssh", 22) is False


"""@pytest.mark.noci
@pytest.mark.timeout(60)
@pytest.mark.module
def test_download_files():
    module = FTPAnonymousAccess()
    hostname = "speedtest.tele2.net"

    port = 21
    try:
        module.execute(hostname, port)
    except OSError as e:
        warnings.warn("Unable to complete test - OSError " + e)
        return
    port = str(port)

    download_path = config.get_module_cache(module.name, hostname, port)

    assert len(os.listdir(download_path)) > 0


@pytest.mark.timeout(15)
@pytest.mark.noci
@pytest.mark.module
def test_download_files():
    module = FTPAnonymousAccess()
    hostname = "speedtest.tele2.net"

    port = 21
    module.execute(hostname, port)
    port = str(port)
    filename = "1KB.zip"

    download_path = config.get_module_cache(module.name, hostname, port)

    assert len(os.listdir(download_path)) > 0

    module = FTPAnonymousAccess()
    try:
        ftp_client = ftplib.FTP()
        ftp_client.connect("speedtest.tele2.net", 21, timeout=15)
        ftp_client.login()
        ftp_files = ftp_client.nlst()
        # 2048 bytes is only bigger than one of the files available - 1KB.zip
        module.download_file(hostname, port, ftp_client, filename)
        local_filename = os.path.join(config.get_module_cache(module.name, hostname, port), filename)
        assert os.path.exists(local_filename)
        ftp_client.quit()
    except TimeoutError:
        warnings.warn("Connection timed out. Test unable to complete")"""


@pytest.mark.noci
@pytest.mark.module
def test_remove_files_over_size():
    module = FTPAnonymousAccess()
    try:
        ftp_client = ftplib.FTP()
        ftp_client.connect("speedtest.tele2.net", 21, timeout=15)
        ftp_client.login()
        ftp_files = ftp_client.nlst()
        # 2048 bytes is only bigger than one of the files available - 1KB.zip
        sanitised_ftp_files, large_files = module.remove_files_over_size(ftp_client, ftp_files, 2048)
        assert len(sanitised_ftp_files) is 1
        ftp_client.quit()
    except TimeoutError:
        warnings.warn("Connection timed out. Test unable to complete")
    except ftplib.error_temp as e:
        warnings.warn("Unable to connect - " + e.args[0])


@pytest.mark.module
def test_unreachable_target():
    module = FTPAnonymousAccess()
    Loot.reset()

    hostname = "127.0.0.1"
    port = 2121

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None
    assert "Downloaded Files" not in Loot.loot[hostname][port][module.loot_name]
    assert "Files" not in Loot.loot[hostname][port][module.loot_name]


@pytest.mark.module
def test_invalid_target():
    module = FTPAnonymousAccess()
    Loot.reset()

    hostname = "256.128.64.32"
    port = 10

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None
    assert "Downloaded Files" not in Loot.loot[hostname][port][module.loot_name]
    assert "Files" not in Loot.loot[hostname][port][module.loot_name]


@pytest.mark.module
def test_invalid_target():
    module = FTPAnonymousAccess()
    Loot.reset()

    hostname = "1.1.1.1"
    port = 21

    module.execute(hostname, port)

    port = str(port)

    assert Loot.loot[hostname] is not None
    assert Loot.loot[hostname][port] is not None
    assert Loot.loot[hostname][port][module.loot_name] is not None
    assert "Downloaded Files" not in Loot.loot[hostname][port][module.loot_name]
    assert "Files" not in Loot.loot[hostname][port][module.loot_name]

