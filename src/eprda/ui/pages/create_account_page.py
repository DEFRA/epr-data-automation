from __future__ import annotations
import asyncio
from playwright.async_api import Page, expect
from sqlalchemy import Enum
from eprda.clients.notifications_client import get_notification_response, get_verification_code
from .base_page import BasePage
from eprda.config.config_loader import Secrets


# ==========================================================
# Enums
# ==========================================================
class YesNo(Enum):
    YES = "Yes"
    NO = "No"

# ==========================================================
# CreateAccountPage
# ==========================================================
class CreateAccountPage(BasePage):
    secrets: Secrets
    def __init__(self, page: Page):
        super().__init__(page)
        self.secrets = Secrets()
        self.email_input = page.locator("#email")
        self.send_verification_code_button = page.locator("#emailVerificationControl_but_send_code")
        self.verification_code_input = page.locator("#verificationCode")
        self.verify_code_button = page.locator("#emailVerificationControl_but_verify_code")
        self.new_password_input = page.locator("#newPassword")
        self.retype_password_input = page.locator("#reenterPassword")
        self.create_button = page.locator("button#continue")

    async def create_producer_account(self, email: str) -> RegisteredCharityPage:
        await self.email_input.fill(email)
        await self.send_verification_code_button.click()
        await asyncio.sleep(1)
        notification_response = await get_notification_response(
            target_email=email, issuer=self.secrets.ISSUER, secret=self.secrets.SECRET
        )

        verification_code = get_verification_code(notification_response)
        print(f"Email: {email}")
        print(f"Verification code retrieved: {verification_code}")
        
        await self.verification_code_input.fill(verification_code)
        await asyncio.sleep(1)
        await self.verify_code_button.click()

        await self.new_password_input.fill("Password123")
        await self.retype_password_input.fill("Password123")
        await asyncio.sleep(1)
        await self.create_button.click()
        return RegisteredCharityPage(self.page)

# ==========================================================
# RegisteredCharityPage
# ==========================================================
class RegisteredCharityPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page) 
        self.continue_button = page.locator("button:has-text('Continue')")

    async def select_is_organisation_registered_charity(self, option: YesNo) -> RegisteredWithCompaniesHousePage:
        selector = f"input[name='isTheOrganisationCharity'][value='{option}']"
        await self.page.locator(selector).click()
        await self.continue_button.click()
        return RegisteredWithCompaniesHousePage(self.page)

# ==========================================================
# RegisteredWithCompaniesHousePage
# ==========================================================
class RegisteredWithCompaniesHousePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.locator("button:has-text('Continue')")

    async def select_is_organisation_registered_with_company_house(self, option: YesNo) -> CompaniesHouseNumberPage:
        selector = f"input[name='IsTheOrganisationRegistered'][value='{option}']"
        await self.page.locator(selector).click()
        await self.continue_button.click()
        return CompaniesHouseNumberPage(self.page)

# ==========================================================
# CompaniesHouseNumberPage
# ==========================================================
class CompaniesHouseNumberPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.company_house_number_input = page.locator("#CompaniesHouseNumber")
        self.continue_button = page.locator("button:has-text('Continue')")
    
    async def enter_companies_house_number(self, company_number: str) -> ConfirmCompanyDetailsPage:
        await self.company_house_number_input.fill(company_number)
        await self.continue_button.click()
        return ConfirmCompanyDetailsPage(self.page)

# ==========================================================
# ConfirmCompanyDetailsPage
# ==========================================================
class ConfirmCompanyDetailsPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.confirm_org_details = page.locator("text=Confirm your organisation’s details from Companies House")
        self.continue_button = page.locator("button:has-text('Continue')")

    async def confirm_company_details(self) -> OrganisationNationPage:
        await expect(self.confirm_org_details).to_be_visible()
        await self.continue_button.click()
        return OrganisationNationPage(self.page)

# ==========================================================
# OrganisationNationPage
# ==========================================================
class OrganisationNationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.locator("button:has-text('Continue')")

    class UKNations(Enum):
        ENGLAND = "England"
        SCOTLAND = "Scotland"
        WALES = "Wales"
        NORTHERN_IRELAND = "Northern Ireland"
           
    async def select_organisation_nation(self, option: "UKNations") -> RoleInOrganisationPage:
        selector = f"input[name='UkNation'][value='{option}']"
        await self.page.locator(selector).click()
        await self.continue_button.click()
        return RoleInOrganisationPage(self.page)

# ==========================================================
# RoleInOrganisationPage
# ==========================================================
class RoleInOrganisationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.locator("button:has-text('Continue')")
          
    class ROLES(Enum):
        DIRECTOR = "Director"
        COMPANY_SECRETARY = "Company Secretary"
        PARTNER = "Partner"
        MEMBER = "Member"
        NONE_OF_THE_ABOVE = "None of the above"
   
    async def select_role_in_organisation(self, option: "ROLES") -> FullNamePage:
        selector = f"input[name='RoleInOrganisation'][value='{option}']"
        await self.page.locator(selector).click()
        await self.continue_button.click()
        return FullNamePage(self.page)

# ==========================================================
# FullNamePage
# ==========================================================
class FullNamePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("#FirstName")
        self.last_name_input = page.locator("#LastName")
        self.continue_button = page.locator("button:has-text('Continue')")

    async def enter_first_name(self, firstName: str):
        await self.first_name_input.fill(firstName)

    async def enter_last_name(self, lastName: str):
        await self.last_name_input.fill(lastName)

    async def enter_full_name(self, firstName: str, lastName: str) -> TelephoneNumberPage:
        await self.enter_first_name(firstName)
        await self.enter_last_name(lastName)
        await self.continue_button.click()
        return TelephoneNumberPage(self.page)

# ==========================================================
# TelephoneNumberPage
# ==========================================================
class TelephoneNumberPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.telephone_number_input = page.locator("#TelephoneNumber")
        self.continue_button = page.locator("button:has-text('Continue')")
    
    async def enter_telephone_number(self, telephoneNumber: str) -> CheckYourDetailsPage:
        await self.telephone_number_input.fill(telephoneNumber)
        await self.continue_button.click()
        return CheckYourDetailsPage(self.page)

# ==========================================================
# CheckYourDetailsPage
# ==========================================================
class CheckYourDetailsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.check_your_details_heading = page.locator("text=Check your details")
        self.continue_button = page.locator("button:has-text('Continue')")

    async def check_your_details(self) -> DeclarationPage:
        await expect(self.check_your_details_heading).to_be_visible()
        await self.continue_button.click()
        return DeclarationPage(self.page)

# ==========================================================
# DeclarationPage
# ==========================================================
class DeclarationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.confirm_and_create_button = page.get_by_role("button", name="Confirm details and create account")

    async def click_confirm_details_and_create_account(self) -> LandingPage:
         await self.confirm_and_create_button.click()
         return LandingPage(self.page)

# ==========================================================
# LandingPage
# ==========================================================
class LandingPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.locator("button.govuk-button:not([id])", has_text="Continue")
        
    async def verify_account_creation(self) -> UsingCompliancePage:
        await expect(self.page.locator("#govuk-notification-banner-title")).to_have_text("Success")
        await self.continue_button.click()
        return UsingCompliancePage(self.page)

# ==========================================================
# UsingCompliancePage
# ==========================================================
class UsingCompliancePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.locator("button.govuk-button:not([id])", has_text="Continue")

    class UsingCompliance(Enum):
        YES = "true"
        NO = "false"

    async def select_is_organisation_registered_charity(self, option: "UsingCompliance"):
        from src.eprda.ui.pages.direct_producer_dashboard_page import DirectProducerDashboardPage
        selector = f"input[name='UsingComplianceScheme'][value='{option}']"
        await self.page.locator(selector).click()
        await self.continue_button.click()
        return DirectProducerDashboardPage(self.page)
    
    