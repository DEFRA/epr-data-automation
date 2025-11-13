import asyncio
from eprda.config.config_loader import EnvConfig
from eprda.utils.file_util import rand_suffix
from eprda.flows.dp_enrolment_flow import create_dp_enrolment_flow, regulator_accept_approved_person
from eprda.flows.dp_registration_submission_flow import dp_submit_registration_data_flow


async def main():
    rand_value = rand_suffix()
    email = f"Automation+{rand_value}@example.test"
    
    # Initialize configuration (loads .env and .secrets automatically)
    envConfig = EnvConfig()

    # Generate a random email
    rand_value = rand_suffix()
    email = f"Automation+{rand_value}@example.test"

    # Run the enrolment flow using environment URLs
    result = await create_dp_enrolment_flow(envConfig.getConfig("PRODUCER_BASE_URL"), email)
    
    await regulator_accept_approved_person(envConfig.getConfig("REGULATOR_BASE_URL"), envConfig.getConfig("REGULATOR_EMAIL"), envConfig.getConfig("REGULATOR_PASSWORD"), result.company_name)

    await dp_submit_registration_data_flow(envConfig.getConfig("PRODUCER_BASE_URL"), email, "Password123", result.organisation_id, result.company_name, result.company_number)

if __name__ == "__main__":
    asyncio.run(main())
