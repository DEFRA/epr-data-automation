from dataclasses import dataclass
from eprda.ui.browser import launch_browser
from eprda.ui.pages.registration_page import RegistrationTaskListPage
from eprda.ui.pages.regulator_home_page import RegulatorHomePage, YesNoOption
from eprda.ui.pages.signin_page import SigninPage
from eprda.utils.csv_factory import create_csv_from_template, TEMPLATES_DIR, OUTPUT_DIR
from anyio import Path
from src.eprda.ui.pages.direct_producer_dashboard_page import DirectProducerDashboardPage

@dataclass
class EnrolmentResult:
    organisation_id: str
    email: str
    company_name: str
    company_number: str

async def create_org_file(org_id: str, organisation_name: str, companies_house_number: str) -> Path:
    template = TEMPLATES_DIR / "org-file-template.csv"
    output = OUTPUT_DIR / f"org_{org_id}.csv"

    rows = [
        {
            "organisation_id": org_id,
            "organisation_name": organisation_name,
            "companies_house_number": companies_house_number,
        }
    ]

    written = create_csv_from_template(template_csv=template, output_csv=output, rows=rows)
    print(f"✅ ORG CSV created: {written.resolve()}")
    return output

async def dp_submit_registration_data_flow(producer_base_url: str, email: str, password: str, org_id: str, organisation_name: str, companies_house_number: str):
    page, ctx, br = await launch_browser(headed=True)
    try:
        await page.goto(producer_base_url)
        signin_page = SigninPage(page)
        await signin_page.login(email, password)
        direct_producer_dashboard_page = DirectProducerDashboardPage(page)
        registration_guidance_page = await direct_producer_dashboard_page.click_registration_for_year_link("2026")
        registration_task_list_page = await registration_guidance_page.click_continue_button()
        upload_organisation_details_page = await registration_task_list_page.click_submit_registration_data_link()

        org_file_path = await create_org_file(org_id, organisation_name, companies_house_number)
        organisation_details_uploaded_page = await upload_organisation_details_page.upload_organisation_details_file(org_file_path)
                                                                                                                     
        await organisation_details_uploaded_page.verify_organisation_details_uploaded()
        review_organisation_data_page = await organisation_details_uploaded_page.click_continue_button()
        await review_organisation_data_page.review_organisation_data()
        declaration_page = await review_organisation_data_page.select_and_confirm_submit_org_details()
        organisation_details_confirmation_page = await declaration_page.enter_full_name_and_click_submit_button("Automation Tester")        
        await organisation_details_confirmation_page.verify_org_details_submission_status()

    except Exception as e:
        print(f"Test failed: {e}")
        await page.screenshot(path="output/submit_regisration_data.png")
        raise Exception(f"Test failed: {e}")
    finally:
        await ctx.close()
        await br.close()
        
async def dp_complete_registration_submission_flow(producer_base_url: str, email: str, password: str):
    page, ctx, br = await launch_browser(headed=True)
    try:
        await page.goto(producer_base_url)
        signin_page = SigninPage(page)
        await signin_page.login(email, password)
        direct_producer_dashboard_page = DirectProducerDashboardPage(page)
        await direct_producer_dashboard_page.click_registration_for_year_link("2026")
        registration_task_list_page = RegistrationTaskListPage(page)
        registration_fee_calculations_page = await registration_task_list_page.click_view_registration_fee_link()
        await registration_fee_calculations_page.verify_registration_fee_text()
        select_payment_options_page = await registration_fee_calculations_page.click_continue_button()
        await select_payment_options_page.verify_how_to_pay_your_registration_fee_heading_text()
        await select_payment_options_page.choose_pay_by_bank_transfer()
        pay_by_bank_transfer_page = await select_payment_options_page.click_continue_button()
        
        await pay_by_bank_transfer_page.verify_registration_fee_due_text()
        direct_producer_dashboard_page = await pay_by_bank_transfer_page.click_continue_button()

        await direct_producer_dashboard_page.click_registration_for_year_link("2026")
        registration_task_list_page = RegistrationTaskListPage(page)
        additional_information_page = await registration_task_list_page.click_submit_registration_application_link()
        submit_registration_request_page = await additional_information_page.click_submit_registration_application_button()
        await submit_registration_request_page.verify_registration_submitted_for_approval_heading_text()
        await submit_registration_request_page.get_application_reference_number()
        registration_task_list_page = await submit_registration_request_page.click_back_button()
    
    except Exception as e:
        print(f"Test failed: {e}")
        await page.screenshot(path="output/submit_regisration_data.png")
        raise Exception(f"Test failed: {e}")
    finally:
        await ctx.close()
        await br.close()
        
async def regulator_accept_registration_submission(regulator_base_url: str, email: str, password: str, company_name: str):
    page, ctx, br = await launch_browser(headed=True)
    try:
        await page.goto(regulator_base_url)
        signin_page = SigninPage(page)
        await signin_page.login(email, password)
        regulator_home_page = RegulatorHomePage(page)
        manage_registration_submissions_page = await regulator_home_page.click_manage_registration_submissions_link()
        await manage_registration_submissions_page.search_organisation_name(company_name)
        registration_submission_details_page = await manage_registration_submissions_page.select_organisation(company_name)
        manage_registration_submissions_grant_page = await registration_submission_details_page.click_grant_registration_button()        
        registration_submission_details_page = await manage_registration_submissions_grant_page.select_grant_registration_confirmation(YesNoOption.YES) 
        await registration_submission_details_page.click_back_button()
        await manage_registration_submissions_page.search_organisation_name(company_name)
        await manage_registration_submissions_page.get_reference_number()
        
    except Exception as e:
        print(f"Test failed: {e}")
        await page.screenshot(path="output/regulator_accept_approved_failed.png")
        raise Exception(f"Test failed: {e}")
    finally:
        await ctx.close()
        await br.close()
