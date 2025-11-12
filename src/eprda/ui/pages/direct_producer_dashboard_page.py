import re
from playwright.async_api import Page, expect
from .registration_page import RegistrationGuidancePage
from .signin_page import SigninPage
from .base_page import BasePage

# ==========================================================
# DirectProducerHomePage
# ==========================================================
class DirectProducerDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.organisation_id = page.locator("p.govuk-body", has_text="Organisation ID:")
        self.report_packaging_data_link = page.locator('a[href="/report-data/file-upload-sub-landing"]')

    async def get_organisation_id(self, company_name: str) -> str:
        company_name_upper = company_name.upper()
        await expect(self.page.locator("h1", has_text=f"Account home - {company_name_upper}")).to_be_visible()
        
        org_text = await self.organisation_id.inner_text()
        match = re.search(r"Organisation ID:\s*([\d ]+)", org_text)
        if not match:
            raise ValueError("Organisation ID not found on the page")

        organisation_id_value = match.group(1).replace(" ", "")
        return organisation_id_value

    async def logout(self) -> "SigninPage":
        await self.page.get_by_role("link", name="Sign out").click()
        await expect(self.page.get_by_role("heading", name="Signed out")).to_be_visible()
        return SigninPage(self.page)
    
    async def click_registration_for_year_link(self, year: str) -> RegistrationGuidancePage:
        await self.page.locator(f"a[href$='registrationyear={year}']").click()
        return RegistrationGuidancePage(self.page)
        
    async def click_report_packaging_data_link(self):
        from src.eprda.ui.pages.report_packaging_data_page import ReportPackagingDataPage
        await self.report_packaging_data_link.click()
        return ReportPackagingDataPage(self.page)
