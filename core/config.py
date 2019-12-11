# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions

    This is the config module.
    This holds all of the key information which should be accessed globally across Lancer.
"""

# Make sure to update the README.MD when changing this
__version__ = "0.1.0 Alpha"

from core import ArgHandler
from core.LogFormatter import LogFormatter

import os
import configparser
import pathlib
import logging
import datetime


class Config(object):
    # TODO: Make class instance
    pass


def get_config_parser() -> configparser.ConfigParser:
    """
    Get the config parser
    :return: Config parser with default values
    """
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg['Main'] = {}
    cfg.set('Main', '# Language for Lancer to be in. Use language code', None)
    cfg['Main']['Language'] = 'en'
    cfg.set('Main', '# Show the Lancer header. \'yes\' or \'no\'', None)
    cfg['Main']['ShowHeader'] = 'yes'
    cfg.set('Main', '# Set the cache notification size', None)
    cfg['Main']['CacheNotificationSize'] = '512'
    cfg.set('Main', '# Set the cache warning size', None)
    cfg['Main']['CacheWarningSize'] = '2048'

    # TODO: Stop convert to lowercase
    # cfg.optionxform = str
    return cfg


def save_config() -> None:
    """
    Write the config file to disk
    """
    global config

    config_file_path = get_config_path()
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)


def load_config() -> None:
    """
    Load the config file from disk. If it doesn't exist, a default one is written to disk anyway
    """
    global config

    config_file_path = get_config_path()

    if not os.path.exists(config_file_path):
        # Write the default settings to file
        save_config()

    config.read(config_file_path)


def module_enabled(name: str) -> bool:
    """
    Checks if a module is enabled. Wrapper for get_module_value(name, "enabled", "yes")
    :param name: The name of the module. Use self.name or module.name
    :return: Boolean if the module is enabled or not
    """
    global config
    return get_module_value(name, "enabled", "yes") == "yes"


def get_cache_notification_size() -> int:
    """
    Get the size of the cache after which we display a notification
    :return: Size of the cache notification size in MB
    """
    global config
    return int(config["CacheNotificationSize"])


def get_cache_warning_size() -> int:
    """
    Get the size of the cache after which we display a warning
    :return: Size of the cache warning size in MB
    """
    global config
    return int(config["CacheWarningSize"])


def get_module_value(name: str, value: str, default: str = "") -> str:
    """
    Get the value held for a specific module in the config.ini file

    :param name: The name of the module
    :param value: The dictionary value you want to get
    :param default: The default value to return if that is not found
    :return: The value held in the dictionary - if not found the default value will be returned instead
    """
    global config

    if name not in config:
        config[name] = {}
    if value not in config[name]:
        config[name][value] = default
    return config[name][value]


def get_lancer_conf_dir() -> str:
    """
    Gets the Lancer configuration directory
    :return: Path to to ~/.lancer/
    """
    # Convert pathlib.Path.home() to str to avoid join error
    # as pathlib.Path.home() appears to be a PosixPath instead
    # of a string in Python 3.5
    # TODO: Remove str() when dropping Python 3.5 support
    path = os.path.join(str(pathlib.Path.home()), ".lancer")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_config_path() -> str:
    """
    Get the config.ini path
    :return: Path to ~/.lancer/config.ini
    """
    return os.path.join(get_lancer_conf_dir(), "config.ini")


def get_cache_path() -> str:
    """
    Get the cache path
    :return: Path to ~/.lancer/cache/
    """
    path = os.path.join(get_lancer_conf_dir(), "cache")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_current_cache_path() -> str:
    """
    Get the current cache path
    :return: Path to ~/.lancer/cache/[SCAN TIME]/
    """
    global folder_name

    path = os.path.join(get_cache_path(), folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_log_path() -> str:
    """
    Get the path to the current log
    :return: Path to ~/.lancer/cache/[SCAN TIME]/lancer.log
    """
    global folder_name

    return os.path.join(get_current_cache_path(), "lancer.log".format(TIME=folder_name))


def get_current_target_cache(target: str) -> str:
    """
    Get the path to the current target cache
    :return: Path to ~/.lancer/cache/[SCAN TIME]/[TARGET]/
    """
    path = os.path.join(get_current_cache_path(), target)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_module_cache(name: str, target: str, port: str = "") -> str:
    """
    Get the path to the current module cache
    :return: Path to ~/.lancer/cache/[SCAN TIME]/[TARGET]/[MODULE]/[PORT]/ or
    ~/.lancer/cache/[SCAN TIME]/[TARGET]/[MODULE]/ if no port is provided
    """
    path = os.path.join(get_current_target_cache(target), name)
    if not os.path.exists(path):
        os.mkdir(path)
    if port != "":
        path = os.path.join(path, port)
        if not os.path.exists(path):
            os.mkdir(path)
    return path


def get_report_folder() -> str:
    """
    Get the path to the current report folder
    :return: Path to ~/.lancer/cache/[SCAN TIME]/reports/
    """
    path = os.path.join(get_current_cache_path(), "reports")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the current module/class
    :param name: The name of the logger - this appears in the logs
    :return: Logger instance to store
    """
    logger = logging.getLogger(name)
    console_logger = logging.StreamHandler()
    console_logger.setFormatter(LogFormatter())
    console_logger.setLevel(logging.WARNING)

    if ArgHandler.get_verbose():
        console_logger.setLevel(logging.INFO)
    elif ArgHandler.get_very_verbose():
        console_logger.setLevel(logging.DEBUG)

    logger.addHandler(console_logger)

    logger.debug("New logger created: {NAME}".format(NAME=name))

    return logger


config = get_config_parser()
current_target = None

folder_name = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

logging.basicConfig(filename=get_log_path(),
                    filemode='w',
                    level=logging.DEBUG,
                    format='[%(asctime)s - %(levelname)s - %(name)s] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')
