#  -*- coding: utf-8 -*-
#
#  """
#      Copyright (c) 2019 Lancer developers
#      See the file 'LICENCE' for copying permissions
#  """
#

"""from modules.legacy import ftp

import ftplib
from core import ArgHandler, config
import warnings
import os


def test_ftp_quiet():
    ArgHandler.parse_arguments(["-T", "127.0.0.1", "-q"])
    ftp.ftp(None)


def test_remove_files_over_size():
    try:
        ftp_client = ftplib.FTP('speedtest.tele2.net')
        ftp_client.login()

        try:
            ftp_files = ftp_client.nlst()
            # 2048 bytes is only bigger than one of the files available - 1KB.zip
            sanitised_ftp_files, large_files = ftp.remove_files_over_size(ftp_client, ftp_files, 2048)
            assert len(sanitised_ftp_files) is 1
        except ftplib.error_temp:
            warnings.warn("Unable to access FTP server from this IP")
        ftp_client.close()
    except TimeoutError:
        warnings.warn("speedtest.tele2.net timed out")


def test_download_file():
    # TODO: Clean ftp directory
    config.current_target = "speedtest.tele2.net"
    try:
        ftp_client = ftplib.FTP('speedtest.tele2.net')
        ftp_client.login()

        try:
            ftp.download_file(ftp_client, '1KB.zip')
            assert os.path.exists(os.path.join(os.path.join("ftp", config.current_target), "1KB.zip"))
        except ftplib.error_temp:
            warnings.warn("Unable to access FTP server from this IP")
        ftp_client.close()
    except TimeoutError:
        warnings.warn("speedtest.tele2.net timed out")


""""""def test_download_files():
    # TODO: Clean ftp directory
    try:
        ftp_client = ftplib.FTP('speedtest.tele2.net')
        ftp_client.login()

        try:
            ftp.download_files(ftp_client)
            assert os.path.exists(os.path.join(os.path.join("ftp", config.args.target), "1KB.zip"))
            assert os.path.exists(os.path.join(os.path.join("ftp", config.args.target), "1MB.zip"))
            assert os.path.exists(os.path.join(os.path.join("ftp", config.args.target), "50MB.zip")) is False

            ftp_client.close()
        except ftplib.error_temp:
            warnings.warn("Unable to access FTP server from this IP")
            ftp_client.close()
    except TimeoutError:
        warnings.warn("speedtest.tele2.net timed out")"""
