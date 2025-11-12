from playwright.async_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def goto(self, url: str):
        await self.page.goto(url)

    async def assert_heading(self, name: str):
        await expect(self.page.get_by_role("heading", name=name)).to_be_visible()