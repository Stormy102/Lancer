import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-modules", action="store_true", default=False, help="Run the module tests only"
    )
    parser.addoption(
        "--run-core", action="store_true", default=False, help="Run the core tests only"
    )
    parser.addoption(
        "--run-no-ci", action="store_true", default=False, help="Run the tests which cannot be run on Travis"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):

    # TODO: Tests for modules that are not run by default
    if not config.getoption("--run-no-ci"):
        skip_non_travis = pytest.mark.skip(reason="Non-Travis tests do not run by default - run with --run-no-ci"
                                                  " to run these tests.")
        for item in items:
            if "noci" in item.keywords:
                item.add_marker(skip_non_travis)

    if config.getoption("--run-modules"):
        skip_not_module = pytest.mark.skip(reason="Only running module tests - run with no args to run all tests")
        for item in items:
            if "module" not in item.keywords:
                item.add_marker(skip_not_module)

    if config.getoption("--run-core"):
        skip_not_core = pytest.mark.skip(reason="Only running core tests - run with no args to run all tests")
        for item in items:
            if "core" not in item.keywords:
                item.add_marker(skip_not_core)
