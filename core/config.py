# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

    This is the config module.
    This holds all of the key information which should be accessed globally across Lancer.
"""

# Make sure to update the README.MD when changing this
__version__ = "0.0.3 Alpha"

from core import utils

import argparse
import os
import configparser
import pathlib
import logging
import datetime


# TODO: Make class instance

def get_config_parser():
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg['Main'] = {}
    cfg.set('Main', '# Language for Lancer to be in. Use language code', None)
    cfg['Main']['Language'] = 'en'
    cfg.set('Main', '# Show the Lancer header. \'yes\' or \'no\'', None)
    cfg['Main']['ShowHeader'] = 'yes'
    cfg.set('Main', '# The directory that the nmap output files should be saved to. Defaults to relative ./nmap '
                    'directory', None)
    cfg['Main']['NmapCache'] = 'nmap'

    cfg.set('Main', '', None)
    cfg.set('Main', '# Below here, you can add your own configuration. This varies module to module, but all modules'
                    ' check if they are enabled.', None)
    cfg.set('Main', '# If you want to disable a module, create a section with [Module Name] and set \"enabled\" to'
                    ' \"false\"', None)
    cfg.set('Main', '# [FTP Banner]', None)
    cfg.set('Main', '# enabled=false', None)

    cfg['FTP Banner'] = {}
    cfg['FTP Banner']['Enabled'] = False

    cfg['File'] = {}
    cfg.set('File', '# The directory that the downloaded FTP files should be saved to. Defaults to relative ./ftp '
                    'directory', None)
    cfg['File']['FTPCache'] = 'ftp'

    cfg['Web'] = {}
    cfg.set('Web', '# The directory that the gobuster output files should be saved to. Defaults to relative ./gobuster '
                   'directory', None)
    cfg['Web']['GobusterCache'] = 'gobuster'
    cfg.set('Web', '# The wordlist that is used by Gobuster when enumerating a HTTP/HTTPS service', None)
    cfg['Web']['DefaultWordlist'] = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'
    cfg.set('Web', '# The directory that the Nikto output files should be saved to. Defaults to relative ./Nikto '
                   'directory', None)
    cfg['Web']['NiktoCache'] = 'nikto'

    # cfg.optionxform = str
    return cfg


def save_config():
    global config

    config_file_path = get_config_path()
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)


def load_config():
    global config

    config_file_path = get_config_path()

    if not os.path.exists(config_file_path):
        # Write the default settings to file
        save_config()

    config.read(config_file_path)


def module_enabled(name: str) -> bool:
    global config

    if name in config:
        if "enabled" in config[name]:
            return config[name]["enabled"].lower() == "true"
    return True


def get_lancer_conf_dir() -> str:
    # Convert pathlib.Path.home() to str to avoid join error
    # as pathlib.Path.home() appears to be a PosixPath instead
    # of a string in Python 3.5
    # TODO: Remove str() when dropping Python 3.5 support
    path = os.path.join(str(pathlib.Path.home()), ".lancer")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_config_path() -> str:
    return os.path.join(get_lancer_conf_dir(), "config.ini")


def get_log_path() -> str:
    global folder_name

    return os.path.join(get_current_cache_path(), "lancer.log".format(TIME=folder_name))


def get_cache_path() -> str:
    path = os.path.join(get_lancer_conf_dir(), "cache")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_current_cache_path() -> str:
    global folder_name

    path = os.path.join(get_cache_path(), folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_current_target_cache(target: str) -> str:
    path = os.path.join(get_current_cache_path(), target)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_module_cache(name: str, target: str) -> str:
    path = os.path.join(get_current_target_cache(target), name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_report_folder() -> str:
    path = os.path.join(get_current_cache_path(), "reports")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    console_logger = logging.StreamHandler()
    formatter = logging.Formatter(utils.error_message() + ' %(message)s')
    console_logger.setFormatter(formatter)
    console_logger.setLevel(logging.ERROR)

    logger.addHandler(console_logger)

    return logger


args = argparse.Namespace
config = get_config_parser()
current_target = None

folder_name = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

logging.basicConfig(filename=get_log_path(),
                    filemode='w',
                    level=logging.DEBUG,
                    format='[%(asctime)s - %(levelname)s - %(name)s] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')
config_logger = get_logger("config")
config_logger.info("Initialised logger at {TIME}".format(TIME=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')))
