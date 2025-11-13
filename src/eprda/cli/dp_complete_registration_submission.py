import argparse
import asyncio
from eprda.config.config_loader import EnvConfig
from eprda.flows.dp_registration_submission_flow import dp_complete_registration_submission_flow, dp_submit_registration_data_flow, regulator_accept_registration_submission


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--email", required=True, help="Contact email; can include {rand} token")
    args = parser.parse_args()

    # Initialize configuration (loads .env and .secrets automatically)
    envConfig = EnvConfig()
    await dp_complete_registration_submission_flow(envConfig.getConfig("PRODUCER_BASE_URL"), args.email, "Password123")   
                                                   
if __name__ == "__main__":
    asyncio.run(main())
