from eprda.ui.browser import launch_browser
from eprda.ui.pages.signin_page import SigninPage
from eprda.utils.csv_factory import create_csv_from_template, TEMPLATES_DIR, OUTPUT_DIR
from anyio import Path
from src.eprda.ui.pages.direct_producer_dashboard_page import DirectProducerDashboardPage

async def create_pom_file(org_id: str) -> Path:
    template = TEMPLATES_DIR / "pom-file-template.csv"
    output = OUTPUT_DIR / f"pom_{org_id}.csv"

    rows = [
        {
            "organisation_id": org_id
        }
    ]

    written = create_csv_from_template(
        template_csv=template, 
        output_csv=output, 
        rows=rows
    )

    print(f"✅ POM CSV created: {written.resolve()}")
    return output


async def dp_report_packaging_data_flow(
    producer_base_url: str,
    email: str,
    password: str,
    org_id: str
):
    page, ctx, br = await launch_browser(headed=True)
    try:
        # Navigate to the Producer Portal
        await page.goto(producer_base_url)

        # Login
        signin_page = SigninPage(page)
        await signin_page.login(email, password)

        # Navigate through dashboard and report flow
        direct_producer_dashboard_page = DirectProducerDashboardPage(page)
        report_packaging_data_page = await direct_producer_dashboard_page.click_report_packaging_data_link()
        report_data_file_upload_page = await report_packaging_data_page.click_report_packaging_data_for_year_link(
            "January to June 2025 (large producers)"
        )

        # Create and upload the file
        pom_file_path = await create_pom_file(org_id)
        check_warnings_page = await report_data_file_upload_page.upload_report_packaging_data_file(pom_file_path)
        
        # Handle subsequent pages
        await check_warnings_page.click_keep_the_same_file_radio_button()
        file_upload_check_file_and_submit_page = await check_warnings_page.click_continue_button()
        await file_upload_check_file_and_submit_page.verify_packaging_data_uploaded_check_and_submit_text()

        # Submit and verify
        file_upload_submission_declaration_page = await file_upload_check_file_and_submit_page.click_continue_button()
        await file_upload_submission_declaration_page.enter_full_name("Automation Tester")
        file_upload_submission_confirmation_page = await file_upload_submission_declaration_page.click_submit_file_button()
        await file_upload_submission_confirmation_page.verify_packaging_data_submitted_to_regulator_text()

        print("✅ Packaging data submission flow completed successfully.")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        await page.screenshot(path="output/pom_data_submission_data.png")
        raise
    finally:
        await ctx.close()
        await br.close()
