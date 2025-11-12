from __future__ import annotations
from enum import Enum
import re
from playwright.async_api import Page, expect
from .base_page import BasePage

# ==========================================================
# RegulatorHomePage
# ==========================================================
class RegulatorHomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_organisation_name_input = page.locator('a[href="/regulators/manage-account/manage"]')
        self.manage_your_account_link = page.locator('a[href="/regulators/applications"]')
        self.manage_applications_for_approved_and_delegated_people_link = page.locator('a[href="/regulators/applications"]')
        self.manage_registration_submissions_link = page.locator('a[href="/regulators/manage-registration-submissions"]')
        self.manage_packaging_data_submissions_link = page.locator('a[href="/regulators/manage-packaging-data-submissions"]')
        self.manage_organisations_details_submissions_link = page.locator('a[href="/regulators/manage-registrations"]')
        self.manage_organisations_and_their_approved_person_link = page.locator('a[href="/regulators/regulator-search-page"]')
        self.sign_out_link = self.page.locator('a[href="/regulators/Account/SignOut"]')
        
    async def click_manage_your_account_link(self):
        await self.manage_your_account_link.click()

    async def click_manage_applications_for_approved_and_delegated_people_link(self) -> RegulatorApplicationsPage:
        await self.manage_applications_for_approved_and_delegated_people_link.click()
        return RegulatorApplicationsPage(self.page)

    async def click_manage_registration_submissions_link(self) -> ManageRegistrationSubmissionsPage:
        await self.manage_registration_submissions_link.click()
        return ManageRegistrationSubmissionsPage(self.page)
    
    async def click_manage_packaging_data_submissions_link(self):
        await self.manage_packaging_data_submissions_link.click()
    
    async def click_manage_organisation_details_submissions_link(self):
        await self.manage_organisations_details_submissions_link.click()
    
    async def click_manage_organisations_and_their_approved_person_link(self):
        await self.manage_organisations_and_their_approved_person_link.click()    

    async def click_signout_button(self):
        await self.sign_out_link.click()
        
# ==========================================================
# RegulatorApplicationsPage
# ==========================================================        
class RegulatorApplicationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)       
        self.search_organisation_name_input = page.locator("#SearchOrganisationName")
        self.apply_filters_button = page.get_by_role("button", name="Apply filters")
        self.accept_approved_person_button = page.locator("#acceptApprovedPersonButton")
        self.approved_person_accepted_banner = page.locator("#govuk-notification-banner-title")
        
    async def search_organisation_name(self, company_name: str):
        await self.search_organisation_name_input.fill(company_name)
        await self.apply_filters_button.click()
    
    async def accept_approved_person(self, company_name: str):
        row = self.page.locator("tr", has_text=company_name)
        await row.get_by_role("button", name="View").click()
        await self.accept_approved_person_button.click()
        await expect(self.approved_person_accepted_banner).to_have_text("Accepted")
        
# ==========================================================
# ManageRegistrationSubmissionsPage
# ==========================================================        
class ManageRegistrationSubmissionsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)       
        self.search_organisation_name_input = page.locator("#OrganisationName")
        self.apply_filters_button = page.get_by_role("button", name="Apply filters")
        self.organisation_id_and_reference_number = page.locator("td.govuk-table__cell", has_text="Organisation ID and reference number")

    async def search_organisation_name(self, company_name: str):
        await self.search_organisation_name_input.fill(company_name)
        await self.apply_filters_button.click()
        
    async def select_organisation(self, company_name: str) -> RegistrationSubmissionDetailsPage:
        await self.page.get_by_role("link", name=company_name).click()
        return RegistrationSubmissionDetailsPage(self.page)
    
    async def get_reference_number(self) -> str:
        element_text = await self.reference_cell.inner_text()
        # Extract the reference number using regex
        match = re.search(r"R\d{2}[A-Z]{2}\d{10,}", element_text.strip())
        if match:
            reference_number = match.group(0)
            print(f"Reference Number: {reference_number}")
            return reference_number
        else:
            raise ValueError("Reference number not found in table cell text.")

# ==========================================================
# RegistrationSubmissionDetailsPage
# ==========================================================        
class RegistrationSubmissionDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)       
        self.grant_registration_button = page.get_by_role("link", name="Grant registration")
        self.back_button = page.locator('a[href*="/regulators/registration-submission-details/"]')

        
    async def click_grant_registration_button(self) -> ManageRegistrationSubmissionsGrantPage:
        await self.grant_registration_button.click()
        return ManageRegistrationSubmissionsGrantPage(self.page)
    
    async def click_back_button(self) -> ManageRegistrationSubmissionsPage:
        await self.back_button.click()
        return ManageRegistrationSubmissionsPage(self.page)

# ==========================================================
# ManageRegistrationSubmissionsGrantPage
# ==========================================================
class YesNoOption(Enum):
    YES = "Yes"
    NO = "No"
    
class ManageRegistrationSubmissionsGrantPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)       
        self.yes_radio_button = page.locator("#radio-label-accepted-true")
        self.continue_button = page.locator("#grantRegistrationSubmissionButton")
        
    async def select_grant_registration_confirmation(self, option: YesNoOption) -> RegistrationSubmissionDetailsPage:
        if option == YesNoOption.YES:
            await self.page.get_by_label("Yes").check()
        elif option == YesNoOption.NO:
            await self.page.get_by_label("No").check()
        await self.continue_button.click()
        return RegistrationSubmissionDetailsPage(self.page)
        
