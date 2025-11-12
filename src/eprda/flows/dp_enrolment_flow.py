from dataclasses import dataclass
from eprda.ui.browser import launch_browser
from eprda.clients.companies_house import fetch_companies
from eprda.ui.pages.signin_page import SigninPage
from eprda.ui.pages.create_account_page import (
    OrganisationNationPage,
    RoleInOrganisationPage,
    YesNo,
)
from eprda.ui.pages.regulator_home_page import RegulatorHomePage

@dataclass
class EnrolmentResult:
    organisation_id: str
    email: str
    company_name: str
    company_number: str


async def create_dp_enrolment_flow(producer_base_url: str, email: str) -> EnrolmentResult:
    page, ctx, br = await launch_browser(headed=True)
    try:
        await page.goto(producer_base_url)
        
        signin_page = SigninPage(page)
        create_account_page = await signin_page.click_create_new_account()
        registered_charity_page = await create_account_page.create_producer_account(email)
        registered_with_companies_house_page = await registered_charity_page.select_is_organisation_registered_charity(YesNo.NO)
        companies_house_number_page = await registered_with_companies_house_page.select_is_organisation_registered_with_company_house(YesNo.YES)
        
        companies = fetch_companies()
        company_number = companies[0]['company_number']
        company_name = companies[0]['company_name']
        
        confirm_company_details_page = await companies_house_number_page.enter_companies_house_number(company_number)
        organisation_nation_page = await confirm_company_details_page.confirm_company_details()
        role_in_organisation_page = await organisation_nation_page.select_organisation_nation(OrganisationNationPage.UKNations.ENGLAND)
        full_name_page = await role_in_organisation_page.select_role_in_organisation(RoleInOrganisationPage.ROLES.DIRECTOR)
        
        telephone_number_page = await full_name_page.enter_full_name("Automation", "Testing")
        check_your_details_page = await telephone_number_page.enter_telephone_number("07777777777")
        declaration_page = await check_your_details_page.check_your_details()
    
        landing_page = await declaration_page.click_confirm_details_and_create_account()
        using_compliance_page = await landing_page.verify_account_creation()
        direct_producer_dashboard_page = await using_compliance_page.select_is_organisation_registered_charity(using_compliance_page.UsingCompliance.NO)
        
        organisation_id = await direct_producer_dashboard_page.get_organisation_id(company_name)
        print(f"organisation_id: {organisation_id}")
        print(f"company_name: {company_name}")
        print(f"company_number: {company_number}")
        await direct_producer_dashboard_page.logout()
        
        return EnrolmentResult(
            organisation_id=organisation_id,
            email=email,
            company_name=company_name,
            company_number=company_number
        )
    except Exception as e:
        print(f"Test failed: {e}")
        await page.screenshot(path="output/create_enrolment_flow.png")
        raise Exception(f"Test failed: {e}")
    finally:
        await ctx.close()
        await br.close()


async def regulator_accept_approved_person(regulator_base_url: str, email: str, password: str, company_name: str):
    page, ctx, br = await launch_browser(headed=True)
    try:
        await page.goto(regulator_base_url)
        signin_page = SigninPage(page)
        await signin_page.login(email, password)
        regulator_home_page = RegulatorHomePage(page)
        regulator_applications_page = await regulator_home_page.click_manage_applications_for_approved_and_delegated_people_link()
        await regulator_applications_page.search_organisation_name(company_name)
        await regulator_applications_page.accept_approved_person(company_name)
    except Exception as e:
        print(f"Test failed: {e}")
        await page.screenshot(path="output/regulator_accept_approved_failed.png")
        raise Exception(f"Test failed: {e}")
    finally:
        await ctx.close()
        await br.close()
