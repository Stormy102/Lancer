import os
import config


def test_get_config_parser():
    cfg = config.get_config_parser()
    assert cfg is not None
    assert cfg['Main']['Show Header'] is 'yes'


def test_get_config_path():
    path = config.get_config_path()
    assert os.path.exists(os.path.dirname(path))
    from getpass import getuser
    assert getuser() in path


def test_save_config():
    config.save_config()
    assert os.path.exists(config.get_config_path())


def test_load_config():
    config.load_config()
    assert config.config is not None
