from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    producer_base_url: str
    regulator_base_url: str

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            producer_base_url=os.getenv("PRODUCER_BASE_URL", ""),
            regulator_base_url=os.getenv("REGULATOR_BASE_URL", ""),
        )