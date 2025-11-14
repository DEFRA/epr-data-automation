import argparse
import asyncio
from eprda.clients.companies_house import CompaniesHouseClient, CompaniesHouseConfig
from eprda.clients.notifications_client import NotificationsClient, NotificationsConfig
from eprda.config.config import load_config
from eprda.utils.file_util import rand_suffix
from src.eprda.flows.dp_enrolment_flow import create_dp_enrolment_flow, regulator_accept_approved_person
from src.eprda.flows.dp_report_packaging_data_flow import dp_report_packaging_data_flow

async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return enrolment result.")
    parser.add_argument("--env", default="dev15", help="ENV_PROFILE; use Environment profile (dev15/tst1), defaults to 'dev15' if not provided")
    args = parser.parse_args()    

    # Load all config/secrets
    config = load_config(args.env)    

    # Build DI clients from secrets
    ch_client = CompaniesHouseClient(
        CompaniesHouseConfig(api_token=config.secrets.COMPANY_HOUSE_TOKEN)
    )

    notifications_client = NotificationsClient(
        NotificationsConfig(
            issuer=config.secrets.ISSUER,
            secret=config.secrets.SECRET,  
            api_base_url="https://api.notifications.service.gov.uk",
            endpoint="v2/notifications",
        )
    )

    email = f"Automation+{rand_suffix()}@example.test"

    # Run the flow
    result = await create_dp_enrolment_flow(
        producer_base_url=config.env.PRODUCER_BASE_URL,
        email=email,
        ch=ch_client,
        notifications=notifications_client,
    )

    # Regulator acceptance
    await regulator_accept_approved_person(
        regulator_base_url=config.env.REGULATOR_BASE_URL,
        email=config.env.REGULATOR_EMAIL,
        password=config.env.REGULATOR_PASSWORD,
        company_name=result.company_name,
    )

    await dp_report_packaging_data_flow(config.env.PRODUCER_BASE_URL, result.email, "Password123", result.organisation_id)

if __name__ == "__main__":
    asyncio.run(main())
