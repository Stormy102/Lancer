from core import config

import os
import pytest


@pytest.mark.core
def test_get_config_parser():
    cfg = config.get_config_parser()
    assert cfg is not None
    assert cfg['Main']['ShowHeader'] is 'yes'


@pytest.mark.core
def test_get_config_path():
    path = config.get_config_path()
    assert os.path.exists(os.path.dirname(path))
    from getpass import getuser
    assert getuser() in path


@pytest.mark.core
def test_save_config():
    config.save_config()
    assert os.path.exists(config.get_config_path())


@pytest.mark.core
def test_load_config():
    config.load_config()
    assert config.config is not None


@pytest.mark.core
def test_load_config_not_on_disk():
    os.remove(config.get_config_path())
    config.load_config()
    assert config.config is not None
    assert os.path.exists(config.get_config_path())
