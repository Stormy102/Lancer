# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from packaging import version
from core import config

import json
import requests


def get_latest_version() -> (str, bool):
    """
    Get the latest tagged version from Github
    :return: Tag on the latest release on Github
    """
    request = requests.get("https://api.github.com/repos/Stormy102/Lancer/releases")
    json_request = json.loads(request.text)
    # Github is in the format vX.Y.Z(-ALPHA)
    # Strip the v from the beginning of the tag name
    latest_version = json_request[0]["tag_name"][1:]
    if "-" in latest_version:
        latest_version = latest_version[0:latest_version.index("-")]
    prerelease = json_request[0]["prerelease"]
    return latest_version, prerelease


def check_if_update_available(latest_version: str) -> bool:
    """
    Check if the latest version is more up-to-date than the current version
    :param latest_version: Latest version from Github
    :return: Bool if there is an update available or not
    """
    short_current_version = config.__version__[0:config.__version__.index(" ")]
    return version.parse(latest_version) > version.parse(short_current_version)
