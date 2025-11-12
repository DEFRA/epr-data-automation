from __future__ import annotations
import re
from playwright.async_api import Page, expect
from .base_page import BasePage

# ==========================================================
# RegistrationGuidancePage
# ==========================================================
class RegistrationGuidancePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.get_by_role("button", name="Continue")

    async def click_continue_button(self) -> RegistrationTaskListPage:
        await self.continue_button.click()
        return RegistrationTaskListPage(self.page)
    
# ==========================================================
# RegistrationTaskListPage
# ==========================================================

class RegistrationTaskListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.submit_registration_data_link = page.get_by_role("link", name="Submit registration data")
        self.view_registration_fee_link = page.get_by_role("link", name="View registration fee")
        self.submit_registration_application_link = page.get_by_role("link", name="Submit registration application")

    async def click_submit_registration_data_link(self) -> UploadOrganisationDetailsPage:
        await self.submit_registration_data_link.click()
        return UploadOrganisationDetailsPage(self.page)
    
    async def click_view_registration_fee_link(self) -> RegistrationFeeCalculationsPage:
        await self.view_registration_fee_link.click()
        return RegistrationFeeCalculationsPage(self.page)
   
    async def click_submit_registration_application_link(self) -> AdditionalInformationPage:
        await self.submit_registration_application_link.click()
        return AdditionalInformationPage(self.page)
    
# ==========================================================
# UploadOrganisationDetails
# ==========================================================    

class UploadOrganisationDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.choose_file_input = page.locator("#file")
        self.upload_file_button = page.get_by_role("button", name="Upload file")

    async def upload_organisation_details_file(self, csvFilePath) -> OrganisationDetailsUploadedPage:
        await self.choose_file_input.set_input_files(csvFilePath)
        await self.upload_file_button.click()
        return OrganisationDetailsUploadedPage(self.page)

# ==========================================================
# OrganisationDetailsUploadedPage
# ==========================================================
    
class OrganisationDetailsUploadedPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.get_by_role("link", name="Continue")

    async def verify_organisation_details_uploaded(self):
        await expect(self.page.locator("#govuk-notification-banner-title")).to_have_text("Success", timeout=30000)
        await expect(self.page.locator("h3.govuk-notification-banner__heading")).to_have_text("Organisation details uploaded")
    
    async def click_continue_button(self) -> ReviewOrganisationDataPage:
        await self.continue_button.click()
        return ReviewOrganisationDataPage(self.page)

# ==========================================================
# ReviewOrganisationDataPage
# ==========================================================

class ReviewOrganisationDataPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = page.locator("#Back")
        self.files_you_uploaded_heading = page.get_by_role("heading", name="Check files and submit")
        self.submit_org_details_radio_button = page.locator("#SubmitOrganisationDetailsResponse")
        self.confirm_button = page.get_by_role("button", name="Confirm")

    async def review_organisation_data(self):
        await expect(self.files_you_uploaded_heading).to_be_visible()
        
    async def select_submit_org_details_radio_button(self):
        await self.submit_org_details_radio_button.click()
        
    async def click_confirm_button(self):
        await self.confirm_button.click()
    
    async def select_and_confirm_submit_org_details(self) -> DeclarationPage:
        await self.select_submit_org_details_radio_button()
        await self.click_confirm_button()
        return DeclarationPage(self.page)
    
    async def click_back_button(self) -> RegistrationTaskListPage:
        await self.back_button.click()
        return RegistrationTaskListPage(self.page)

# ==========================================================
# DeclarationPage
# ==========================================================

class DeclarationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.full_name_input = page.locator("#FullName")
        self.submit_file_button= page.get_by_role("button", name="Submit file")

    async def enter_full_name(self, full_name: str):
        await self.full_name_input.fill(full_name)

    async def click_submit_file_button(self):
        await self.submit_file_button.click()
        
    async def enter_full_name_and_click_submit_button(self, full_name: str) -> OrganisationDetailsConfirmationPage:
        await self.enter_full_name(full_name)
        await self.click_submit_file_button()
        return OrganisationDetailsConfirmationPage(self.page)

# ==========================================================
# OrganisationDetailsConfirmationPage
# ==========================================================

class OrganisationDetailsConfirmationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.org_details_submission_status = page.get_by_role("heading", name="Organisation details submitted")
        
    async def verify_org_details_submission_status(self):
        await expect(self.org_details_submission_status).to_be_visible()
        
        
# ==========================================================
# RegistrationFeeCalculationsPage
# ==========================================================

class RegistrationFeeCalculationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.registration_fee_heading_text = page.get_by_role("heading", name="Registration fee")
        self.continue_button = page.get_by_role("button", name="Continue")
    
    async def verify_registration_fee_text(self):
        await expect(self.registration_fee_heading_text).to_be_visible()
        
    async def click_continue_button(self) -> SelectPaymentOptionsPage:
        await self.continue_button.click()
        return SelectPaymentOptionsPage(self.page)
    
# ==========================================================
# SelectPaymentOptionsPage
# ==========================================================

class SelectPaymentOptionsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.how_to_pay_your_registration_fee_heading_text = page.get_by_role("heading", name="How to pay your registration fee")
        self.pay_by_bank_transfer_radio_button = page.locator("#PayByBankTransfer")
        self.continue_button = page.get_by_role("button", name="Continue")
    
    async def verify_how_to_pay_your_registration_fee_heading_text(self):
        await expect(self.how_to_pay_your_registration_fee_heading_text).to_be_visible()

    async def choose_pay_by_bank_transfer(self):
        await self.pay_by_bank_transfer_radio_button.click()
    
    async def click_continue_button(self) -> PayByBankTransferPage:
        await self.continue_button.click()
        return PayByBankTransferPage(self.page)

# ==========================================================
# PayByBankTransferPage
# ==========================================================

class PayByBankTransferPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.pay_by_bank_transfer_heading_text = page.get_by_role("heading", name="Pay by bank transfer")
        self.return_to_dashboard_link = page.locator('a[href="/report-data/home-self-managed"]')
    
    async def verify_registration_fee_due_text(self):
        await expect(self.pay_by_bank_transfer_heading_text).to_be_visible()
    
    async def click_continue_button(self):
        from eprda.ui.pages.direct_producer_dashboard_page import DirectProducerDashboardPage
        await self.return_to_dashboard_link.click()
        return DirectProducerDashboardPage(self.page)

# ==========================================================
# AdditionalInformationPage
# ==========================================================

class AdditionalInformationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.submit_registration_application_button = page.get_by_role("button", name="Submit registration application")

    async def click_submit_registration_application_button(self) -> SubmitRegistrationRequestPage:
        await self.submit_registration_application_button.click()
        return SubmitRegistrationRequestPage(self.page)
    
    
# ==========================================================
# submitRegistrationRequestPage
# ==========================================================

class SubmitRegistrationRequestPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.registration_submitted_for_approval_heading_text = page.get_by_role("heading", name=re.compile(r"Your registration application for \d{4} has been submitted for approval"))
        self.application_reference_number = page.locator("div.govuk-panel__body", has_text="Application reference:")
        self.back_button = page.locator("#Back")
        
    async def verify_registration_submitted_for_approval_heading_text(self):
        await expect(self.registration_submitted_for_approval_heading_text).to_be_visible()
    
    async def get_application_reference_number(self) -> str:
        element_text = await self.application_reference_number.inner_text()
        # Extract the reference number from the text
        reference_number = element_text.split("Application reference:")[-1].strip()
        print(f"Application reference number: {reference_number}")
        return reference_number
        
    async def click_back_button(self) -> RegistrationTaskListPage:
        await self.back_button.click()
        return RegistrationTaskListPage(self.page)