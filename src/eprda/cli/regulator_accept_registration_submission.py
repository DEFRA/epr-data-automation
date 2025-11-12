import argparse
import asyncio
import os
from eprda.config.config_loader import load_env, Settings
from eprda.flows.dp_registration_submission_flow import dp_complete_registration_submission_flow, dp_submit_registration_data_flow, regulator_accept_registration_submission


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--env", default=None, help="ENV_PROFILE; default uses ENV_PROFILE or 'dev15'")
    parser.add_argument("--company_name", required=True, default=None, help="Company name")
    args = parser.parse_args()

    # Override environment profile if provided
    if args.env:
        os.environ["ENV_PROFILE"] = args.env

    # Load environment variables
    load_env()
    settings = Settings()
    
    await regulator_accept_registration_submission(settings.regulator_base_url, "environment.dev15E2E+regulator002@eviden.com", "Welc0me15!", args.company_name)

if __name__ == "__main__":
    asyncio.run(main())
