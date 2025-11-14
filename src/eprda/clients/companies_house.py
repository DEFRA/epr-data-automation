from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
import json
import requests

@dataclass(frozen=True)
class CompaniesHouseConfig:
    api_token: str
    base_url: str = "https://stream.companieshouse.gov.uk"
    timeout_s: int = 30

    def auth_header(self) -> str:
        return f"Basic {self.api_token}"

class CompaniesHouseClient:
    def __init__(self, cfg: CompaniesHouseConfig, session: Optional[requests.Session] = None):
        self._cfg = cfg
        self._session = session or requests.Session()

    def fetch_companies(self, max_records: int = 10) -> list[Dict[str, str]]:
        url = f"{self._cfg.base_url}/companies"
        headers = {"Authorization": self._cfg.auth_header()}
        print(f"Headers: {headers}")
        companies: list[Dict[str, str]] = []

        with self._session.get(url, headers=headers, timeout=self._cfg.timeout_s, stream=True) as r:
            r.raise_for_status()
            count = 0
            for line in r.iter_lines():
                if not line:
                    continue
                event = json.loads(line)
                data = event.get("data", {})
                num = data.get("company_number")
                name = data.get("company_name")
                if num and name:
                    companies.append({"company_number": num, "company_name": name})
                    count += 1
                    if count >= max_records:
                        break
        return companies
