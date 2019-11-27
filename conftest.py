import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-modules", action="store_true", default=False, help="Run the module tests only"
    )
    parser.addoption(
        "--run-core", action="store_true", default=False, help="Run the core tests only"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):

    if config.getoption("--run-modules"):
        skip_not_module = pytest.mark.skip(reason="Only running module tests - use --run-core or --all to run")
        for item in items:
            if "module" not in item.keywords:
                item.add_marker(skip_not_module)

    if config.getoption("--run-core"):
        skip_not_core = pytest.mark.skip(reason="Only running core tests - use --run-core or --all to run")
        for item in items:
            if "core" not in item.keywords:
                item.add_marker(skip_not_core)
