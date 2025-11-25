import re
from playwright.async_api import Page, expect
from .registration_page import RegistrationGuidancePage
from .signin_page import SigninPage
from .base_page import BasePage

# ==========================================================
# ManageComplianceSchemePage
# ==========================================================
class ManageComplianceSchemePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.change_or_remove_compliance_sceheme_link = page.locator("a[href='/report-data/change-compliance-scheme-options']")
        self.sign_out_link = page.get_by_role("link", name="Sign out")
        self.organisation_id = page.locator("p.govuk-body", has_text="Organisation ID:")

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
        await self.sign_out_link.click()
        await expect(self.page.get_by_role("heading", name="Signed out")).to_be_visible()
        return SigninPage(self.page)
    
    async def click_report_packaging_data_link(self):
        from src.eprda.ui.pages.change_compliance_scheme_options_page import ChangeComplianceSchemeOptionsPage
        await self.change_or_remove_compliance_sceheme_link.click()
        return ChangeComplianceSchemeOptionsPage(self.page)

