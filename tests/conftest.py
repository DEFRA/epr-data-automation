import os
import pytest
from eprda.config.config_loader import load_env

@pytest.fixture(scope="session", autouse=True)
def _load_env_for_tests():
    load_env()

# Global hooks can go here (e.g., add screenshots on failure)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
