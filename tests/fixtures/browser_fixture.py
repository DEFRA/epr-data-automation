import pytest
from eprda.config.config_loader import load_env, Settings
from eprda.ui.browser import launch_browser

@pytest.fixture(scope="session", autouse=True)
def _load_env():
    load_env()

@pytest.fixture(scope="session")
def settings():
    settings_obj = Settings()
    # Add base_url alias for backward compatibility with tests
    settings_obj.base_url = settings_obj.producer_base_url
    return settings_obj

@pytest.fixture
async def page_ctx(settings):
    page, context, browser = await launch_browser(headed=not settings.headless)
    try:
        yield (page, context, browser)
    finally:
        await context.close()
        await browser.close()
