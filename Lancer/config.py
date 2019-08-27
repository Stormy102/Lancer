#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

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
    cfg.set('Main', '# Language for Lancer to be in. Use language code', None)
    cfg['Main']['Language'] = 'en'
    cfg.set('Main', '# Show the Lancer header. \'yes\' or \'no\'', None)
    cfg['Main']['ShowHeader'] = 'yes'
    cfg.set('Main', '# The directory that the nmap output files should be saved to. Defaults to relative ./nmap'
                    'directory', None)
    cfg['Main']['NmapCache'] = 'nmap'

    cfg['File'] = {}
    cfg.set('File', '# The directory that the downloaded FTP files should be saved to. Defaults to relative ./ftp'
                    'directory', None)
    cfg['File']['FTPCache'] = 'ftp'

    cfg['Web'] = {}
    cfg.set('Web', '# The directory that the gobuster output files should be saved to. Defaults to relative ./gobuster'
                   'directory', None)
    cfg['Web']['GobusterCache'] = 'gobuster'
    cfg.set('Web', '# The wordlist that is used by Gobuster when enumerating a HTTP/HTTPS service', None)
    cfg['Web']['DefaultWordlist'] = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'
    cfg.set('Web', '# The directory that the Nikto output files should be saved to. Defaults to relative ./Nikto'
                   'directory', None)
    cfg['Web']['NiktoCache'] = 'nikto'

    # cfg.optionxform = str
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
    # Convert pathlib.Path.home() to str to avoid join error
    # as pathlib.Path.home() appears to be a PosixPath instead
    # of a string in Python 3.5
    # TODO: Remove str() when dropping Python 3.5 support
    path = os.path.join(str(pathlib.Path.home()), ".lancer")
    if not os.path.exists(path):
        os.mkdir(path)
    return os.path.join(path, "config.ini")


def nmap_cache():
    if args.cache_root != "":
        return os.path.join(args.cache_root, "nmap")

    return config['Main']['NmapCache']


def gobuster_cache():
    if args.cache_root != "":
        return os.path.join(args.cache_root, "gobuster")

    return config['Web']['GobusterCache']


def nikto_cache():
    if args.cache_root != "":
        return os.path.join(args.cache_root, "nikto")

    return config['Web']['NiktoCache']


def ftp_cache():
    if args.cache_root != "":
        return os.path.join(args.cache_root, "ftp")

    return config['File']['FTPCache']


args = argparse.Namespace
config = get_config_parser()
