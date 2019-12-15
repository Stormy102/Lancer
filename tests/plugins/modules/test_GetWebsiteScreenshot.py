# -*- coding: utf-8 -*-

"""
    Copyright (c) 2019 Lancer developers
    See the file 'LICENCE' for copying permissions
"""

from plugins.modules.GetWebsiteScreenshot import GetWebsiteScreenshot
from core import config

import pytest
import os
import glob


@pytest.mark.noci
@pytest.mark.module
def test_take_screenshot():
    module = GetWebsiteScreenshot()

    hostname = "facepunch.com"
    port = 443

    module.execute(hostname, port)

    port = str(port)

    assert len(glob.glob(os.path.join(config.get_module_cache(module.name, hostname, port), "*.png"))) > 0


@pytest.mark.module
def test_take_screenshot_unreachable():
    module = GetWebsiteScreenshot()

    hostname = "127.0.0.1"
    port = 1337

    module.execute(hostname, port)

    port = str(port)

    assert len(glob.glob(os.path.join(config.get_module_cache(module.name, hostname, port), "*.png"))) == 0


@pytest.mark.module
def test_take_screenshot_invalid():
    module = GetWebsiteScreenshot()

    hostname = "256.128.64.32"
    port = 1337

    module.execute(hostname, port)

    port = str(port)

    assert len(glob.glob(os.path.join(config.get_module_cache(module.name, hostname, port), "*.png"))) == 0


@pytest.mark.noci
@pytest.mark.module
def test_take_screenshot_timeout():
    module = GetWebsiteScreenshot()

    hostname = "1.1.1.1"
    port = 1337

    module.execute(hostname, port)

    port = str(port)

    assert len(glob.glob(os.path.join(config.get_module_cache(module.name, hostname, port), "*.png"))) == 0
