from __future__ import annotations
from playwright.async_api import Page
from .base_page import BasePage

class SigninPage(BasePage):
    # -------------------------
    # Class-level locators
    # -------------------------
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    NEXT_BUTTON = "#next"
    CREATE_NEW_ACCOUNT_LINK = "#createAccount"

    def __init__(self, page: Page):
        super().__init__(page)

    async def login(self, email: str, password: str):
        await self.page.locator(self.EMAIL_INPUT).fill(email)
        await self.page.locator(self.PASSWORD_INPUT).fill(password)
        await self.page.locator(self.NEXT_BUTTON).click()
        
    async def click_create_new_account(self):
        from src.eprda.ui.pages.create_account_page import CreateAccountPage
        await self.page.locator(self.CREATE_NEW_ACCOUNT_LINK).click()
        return CreateAccountPage(self.page)
