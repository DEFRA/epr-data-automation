from __future__ import annotations
from playwright.async_api import Page
from sqlalchemy import Enum
from .base_page import BasePage

# ==========================================================
# ChangeComplianceSchemeOptionsPage
# ==========================================================

class ComplianceSchemeOption(Enum):
    CHANGE = "ChooseNewComplianceScheme"
    STOP = "StopComplianceScheme"
   
class ChangeComplianceSchemeOptionsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.continue_button = page.get_by_role("button", name="Continue")

def update_compliance_scheme_changes(self, option: ComplianceSchemeOption):
    self.page.locator(
        f"input.govuk-radios__input[value='{option.value}']"
    ).check()
    self.continue_button.click()


# ==========================================================
# StopUsingComplianceSchemePage
# ==========================================================

class StopUsingComplianceSchemePage(Enum):

    def __init__(self, page: Page):
        super().__init__(page)
        self.remove_compliance_scheme_button = page.get_by_role("button", name="Remove compliance scheme")

    async def update_compliance_scheme_changes(self):
        from src.eprda.ui.pages.direct_producer_dashboard_page import DirectProducerDashboardPage
        self.remove_compliance_scheme_button.click()
        return DirectProducerDashboardPage(self.page)