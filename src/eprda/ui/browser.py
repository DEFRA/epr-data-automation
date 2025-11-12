import os
from playwright.async_api import async_playwright

DEFAULT_BROWSER = "chrome"

BROWSERS = {
    "chrome": {"type": "chromium", "channel": "chrome"},
    "edge": {"type": "chromium", "channel": "msedge"},
    "chromium": {"type": "chromium", "channel": None},
    "firefox": {"type": "firefox", "channel": None},
    "webkit": {"type": "webkit", "channel": None},
}

async def launch_browser(headed=False):
    print(f"🚀 Launching browser: chrome (headed={headed})")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=not headed, args=["--start-maximized"])
    context = await browser.new_context()
    page = await context.new_page()
    return page, context, browser