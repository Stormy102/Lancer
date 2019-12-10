import pytest


def pytest_addoption(parser) -> None:
    """
    Add options to the command line parser
    :param parser: Parser to add items to
    """
    parser.addoption(
        "--run-modules", action="store_true", default=False, help="Run the module tests only"
    )
    parser.addoption(
        "--run-core", action="store_true", default=False, help="Run the core tests only"
    )
    parser.addoption(
        "--run-no-ci", action="store_true", default=False, help="Run the tests which cannot be run on Travis"
    )


def pytest_collection_modifyitems(config, items) -> None:
    """
    Filter the tests by arguments passed:

    - --run-no-ci will run non-default tests not run on public CI servers
    - --run-core will only run the core tests
    - --run-modules will run all module tests
    :param config: Command line parser
    :param items: Test items
    """

    # TODO: Tests for modules that are not run by default
    if not config.getoption("--run-no-ci"):
        skip_non_travis = pytest.mark.skip(reason="Non-Travis tests do not run by default - run with --run-no-ci"
                                                  " to run these tests.")
        for item in items:
            if "noci" in item.keywords:
                item.add_marker(skip_non_travis)

    if config.getoption("--run-modules"):
        skip_not_module = pytest.mark.skip(reason="Only running module tests - run with no args to run all tests")
        mark_skip(items, "module", skip_not_module)

    if config.getoption("--run-core"):
        skip_not_core = pytest.mark.skip(reason="Only running core tests - run with no args to run all tests")
        mark_skip(items, "core", skip_not_core)


def mark_skip(items, keyword: str, skip_marker):
    for item in items:
        if keyword not in item.keywords:
            item.add_marker(skip_marker)
