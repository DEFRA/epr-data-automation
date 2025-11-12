import requests
import json
from eprda.config.config_loader import Secrets

def fetch_companies(max_records=10):
    """
    Fetch company data from Companies House streaming API.
    
    Args:
        max_records (int): Maximum number of records to fetch. Default is 10.
    
    Returns:
        list: List of dictionaries containing 'company_number' and 'company_name'.
    """
    url = "https://stream.companieshouse.gov.uk/companies"
    secrets = Secrets()
    headers = {"Authorization": f"Basic {secrets.COMPANY_HOUSE_TOKEN}"}
    
    companies = []
    
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        count = 0
        for line in r.iter_lines():
            if not line:
                continue
            event = json.loads(line)
            data = event.get("data", {})
            company_number = data.get("company_number")
            company_name = data.get("company_name")
            
            if company_number and company_name:
                companies.append({
                    "company_number": company_number,
                    "company_name": company_name
                })
                count += 1
                if count >= max_records:
                    break
    
    return companies