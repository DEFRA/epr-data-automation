from __future__ import annotations
from playwright.async_api import Page, expect
from .base_page import BasePage

# ==========================================================
# ReportPackagingDataPage
# ==========================================================
class ReportPackagingDataPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.organisation_id = page.locator("p.govuk-body", has_text="Organisation ID:")
 
    async def click_report_packaging_data_for_year_link(self, period_text: str) -> ReportDataFileUploadPage:
        card = self.page.locator("div.submission-period-card", has_text=f"Report packaging data for {period_text}")

        # Click the "Start now" button within that specific card
        await card.get_by_role("button", name="Start now").click()
        return ReportDataFileUploadPage(self.page)

# ==========================================================
# ReportDataFileUploadPage
# ==========================================================
class ReportDataFileUploadPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.choose_file_input = page.locator("#file")
        self.upload_file_button = page.get_by_test_id("pom-data-upload-button")

    async def upload_report_packaging_data_file(self, csvFilePath) -> CheckWarningsPage:
        await self.choose_file_input.set_input_files(csvFilePath)
        await self.upload_file_button.click()
        return CheckWarningsPage(self.page)

# ==========================================================
# CheckWarningsPage
# ==========================================================
class CheckWarningsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.keep_the_same_file_radio_button = page.locator("#UploadNewFile-1")
        self.continue_button = page.get_by_role("button", name="Continue")

    async def click_keep_the_same_file_radio_button(self):
        await self.keep_the_same_file_radio_button.click()

    async def click_continue_button(self) -> FileUploadCheckFileAndSubmitPage:
        await self.continue_button.click()
        return FileUploadCheckFileAndSubmitPage(self.page)

# ==========================================================
# FileUploadCheckFileAndSubmitPage
# ==========================================================
class FileUploadCheckFileAndSubmitPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.packaging_data_uploaded_check_and_submit_text = page.get_by_role("heading", name="Packaging data uploaded – check and submit")
        self.continue_button = page.get_by_role("button", name="Continue")

    async def verify_packaging_data_uploaded_check_and_submit_text(self) -> FileUploadCheckFileAndSubmitPage:
        await expect(self.packaging_data_uploaded_check_and_submit_text).to_be_visible()

    async def click_continue_button(self) -> FileUploadSubmissionDeclarationPage:
        await self.continue_button.click()
        return FileUploadSubmissionDeclarationPage(self.page)
    
# ==========================================================
# FileUploadSubmissionDeclarationPage
# ==========================================================
class FileUploadSubmissionDeclarationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.full_name_input = page.locator("#DeclarationName")
        self.submit_file_button = page.get_by_test_id("submission-declaration-button")

    async def enter_full_name(self, full_name):
        await self.full_name_input.fill(full_name)

    async def click_submit_file_button(self) -> FileUploadSubmissionConfirmationPage:
        await self.submit_file_button.click()
        return FileUploadSubmissionConfirmationPage(self.page)
        
# ==========================================================
# FileUploadSubmissionConfirmationPage
# ==========================================================
class FileUploadSubmissionConfirmationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.packaging_data_submitted_to_regulator_text = page.get_by_role("heading", name="Packaging data submitted to the environmental regulator")

    async def verify_packaging_data_submitted_to_regulator_text(self):
        await expect(self.packaging_data_submitted_to_regulator_text).to_be_visible()