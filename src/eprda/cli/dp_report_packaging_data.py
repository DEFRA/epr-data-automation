import asyncio
from eprda.config.config_loader import EnvConfig
from eprda.utils.file_util import rand_suffix
from src.eprda.flows.dp_enrolment_flow import create_dp_enrolment_flow, regulator_accept_approved_person
from src.eprda.flows.dp_report_packaging_data_flow import dp_report_packaging_data_flow

async def main():
    rand_value = rand_suffix()
    email = f"Automation+{rand_value}@example.test"
    
    # Initialize configuration (loads .env and .secrets automatically)
    envConfig = EnvConfig()

    # Generate a random email
    rand_value = rand_suffix()
    email = f"Automation+{rand_value}@example.test"

    # Run the enrolment flow using environment URLs
    result = await create_dp_enrolment_flow(envConfig.get("PRODUCER_BASE_URL"), email)
    
    result = await create_dp_enrolment_flow(envConfig.getConfig("PRODUCER_BASE_URL"), email)
    await regulator_accept_approved_person(envConfig.getConfig("REGULATOR_BASE_URL"), envConfig.getConfig("REGULATOR_EMAIL"), envConfig.getConfig("REGULATOR_PASSWORD"), result.company_name)
    await dp_report_packaging_data_flow(envConfig.getConfig("PRODUCER_BASE_URL"), result.email, "Password123", result.organisation_id)

if __name__ == "__main__":
    asyncio.run(main())
