"""
    This is the config module.

    This holds all of the key information which should be accessed globally across Lancer.
"""

# Make sure to update the README.MD when changing this
__version__ = "0.0.2 Alpha"

import argparse
import os
import configparser
import pathlib


def get_config_parser():
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg['Main'] = {}
    cfg.set('Main', '; Language for Lancer to be in. Use language code', None)
    cfg['Main']['Language'] = 'en'
    cfg.set('Main', '; Show the Lancer header. \'yes\' or \'no\'', None)
    cfg['Main']['Show Header'] = 'yes'
    cfg.set('Main', '; The directory that the nmap output files should be saved to. Defaults to relative ./nmap'
                    'directory', None)
    cfg['Main']['NmapCache'] = 'nmap'

    cfg['Web'] = {}
    cfg.set('Web', '; The directory that the downloaded FTP files should be saved to. Defaults to relative ./ftp'
                   'directory', None)
    cfg['Web']['FTPCache'] = 'ftp'
    cfg.set('Web', '; The directory that the nmap output files should be saved to. Defaults to relative ./gobuster'
                   'directory', None)
    cfg['Web']['GobusterCache'] = 'gobuster'
    cfg.set('Web', '; The wordlist that is used by Gobuster when enumerating a HTTP/HTTPS service', None)
    cfg['Web']['DefaultWordlist'] = '/usr/share/wordlists/dirbuster/directory-2.3-medium.txt'
    return cfg


def save_config():
    config_file_path = get_config_path()
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)


def load_config():
    config_file_path = get_config_path()

    if not os.path.exists(config_file_path):
        # Write the default settings to file
        save_config()

    config.read(config_file_path)


def get_config_path():
    path = os.path.join(pathlib.Path.home(), ".lancer")
    if not os.path.exists(path):
        os.mkdir(path)
    return os.path.join(path, "config.ini")


args = argparse.Namespace
config = get_config_parser()
