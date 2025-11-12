import argparse
import asyncio
import os
from eprda.config.config_loader import load_env, Settings
from eprda.utils.file_util import rand_suffix
from eprda.flows.dp_enrolment_flow import create_dp_enrolment_flow, regulator_accept_approved_person
from eprda.flows.dp_registration_submission_flow import dp_submit_registration_data_flow


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    # parser.add_argument("--email", required=False, help="Contact email; can include {rand} token")
    # parser.add_argument("--password", required=False, help="Password; default generated")
    parser.add_argument("--env", default=None, help="ENV_PROFILE; default uses ENV_PROFILE or 'dev15'")
    args = parser.parse_args()

    # Override environment profile if provided
    if args.env:
        os.environ["ENV_PROFILE"] = args.env

    # Load environment variables
    load_env()
    settings = Settings()

    rand_value = rand_suffix()
    email = f"Automation+{rand_value}@example.test"

    result = await create_dp_enrolment_flow(settings.producer_base_url, email)
    
    await regulator_accept_approved_person(settings.regulator_base_url, "environment.dev15E2E+regulator002@eviden.com", "Welc0me15!", result.company_name)

    await dp_submit_registration_data_flow(settings.producer_base_url, email, "Password123", result.organisation_id, result.company_name, result.company_number)

if __name__ == "__main__":
    asyncio.run(main())
