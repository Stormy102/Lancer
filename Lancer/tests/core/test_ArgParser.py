from core import ArgHandler, config
import pytest


def test_parse_arguments():
    ArgHandler.parse_arguments(["-T", "127.0.0.1"])
    assert config.args.target is not None


def test_create_parser():
    parser = ArgHandler.create_parser()
    assert parser is not None


def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        ArgHandler.parse_arguments([])