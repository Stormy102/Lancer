import lancerargs
import pytest


def test_create_parser():
    parser = lancerargs.create_parser()
    assert parser is not None


def test_quits_with_no_parameters():
    with pytest.raises(SystemExit):
        lancerargs.parse_arguments([])