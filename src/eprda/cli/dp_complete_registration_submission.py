import argparse
import asyncio
from eprda.config.config import load_config
from eprda.flows.dp_registration_submission_flow import dp_complete_registration_submission_flow, dp_submit_registration_data_flow, regulator_accept_registration_submission


async def main():
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--email", required=True, help="Contact email; can include {rand} token")
    args = parser.parse_args()

    # Load all config/secrets
    config = load_config(args.env)
    await dp_complete_registration_submission_flow(config.env.PRODUCER_BASE_URL, args.email, "Password123")   
                                                   
if __name__ == "__main__":
    asyncio.run(main())
