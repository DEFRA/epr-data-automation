import argparse
import asyncio
from eprda.config.config_loader import EnvConfig
from eprda.flows.dp_registration_submission_flow import regulator_accept_registration_submission


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--company_name", required=True, default=None, help="Company name")
    args = parser.parse_args()
    
    # Initialize configuration (loads .env and .secrets automatically)
    envConfig = EnvConfig()

    await regulator_accept_registration_submission(envConfig.getConfig("REGULATOR_BASE_URL"), envConfig.getConfig("REGULATOR_EMAIL"), envConfig.getConfig("REGULATOR_PASSWORD"), args.company_name)

if __name__ == "__main__":
    asyncio.run(main())
