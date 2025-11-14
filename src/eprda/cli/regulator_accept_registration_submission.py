import argparse
import asyncio
from eprda.config.config import load_config
from eprda.flows.dp_registration_submission_flow import regulator_accept_registration_submission


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return enrolment result.")
    parser.add_argument("--env", default="dev15", help="ENV_PROFILE; use Environment profile (dev15/tst1), defaults to 'dev15' if not provided")
 
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--company_name", required=True, default=None, help="Company name")

    args = parser.parse_args()
    
    # Load all config/secrets
    config = load_config(args.env)

    await regulator_accept_registration_submission(config.env.REGULATOR_BASE_URL, config.env.REGULATOR_EMAIL, config.env.REGULATOR_PASSWORD, args.company_name)

if __name__ == "__main__":
    asyncio.run(main())
