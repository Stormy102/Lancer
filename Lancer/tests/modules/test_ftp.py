from modules import ftp

import ftplib
import warnings
import os


def test_remove_files_over_size():
    ftp_client = ftplib.FTP('speedtest.tele2.net')
    ftp_client.login()

    try:
        ftp_files = ftp_client.nlst()
        # 2048 bytes is only bigger than one of the files available - 1KB.zip
        sanitised_ftp_files = ftp.remove_files_over_size(ftp_client, ftp_files, 2048)
        assert len(sanitised_ftp_files) is 1
    except ftplib.error_temp:
        warnings.warn("Unable to access FTP server from this IP")
    ftp_client.close()


def test_download_file():
    # TODO: Clean ftp directory
    ftp_client = ftplib.FTP('speedtest.tele2.net')
    ftp_client.login()

    try:
        ftp.download_file(ftp_client, '1KB.zip')
        assert os.path.exists('ftp/1KB.zip')
    except ftplib.error_temp:
        warnings.warn("Unable to access FTP server from this IP")
    ftp_client.close()


def test_download_files():
    # TODO: Clean ftp directory
    ftp_client = ftplib.FTP('speedtest.tele2.net')
    ftp_client.login()

    try:
        ftp.download_files(ftp_client)
        assert os.path.exists('ftp/1KB.zip')
        assert os.path.exists('ftp/1MB.zip')
        assert os.path.exists('ftp/50MB.zip') is False
    except ftplib.error_temp:
        warnings.warn("Unable to access FTP server from this IP")
    ftp_client.close()
