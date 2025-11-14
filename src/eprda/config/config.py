import argparse
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[3]
ENV_DIR = ROOT / "config" / "environments"
SECRETS_DIR = ROOT / "config" / "secrets"


def _resolve_profile(profile: Optional[str]) -> str:
    return (profile or os.getenv("ENV_PROFILE") or "dev15").strip()


def _to_bool(raw: Optional[str], default: bool = False) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class EnvConfig:
    _values: Dict[str, str]

    def __getattr__(self, name: str) -> str:
        try:
            return self._values[name]
        except KeyError as exc:
            raise AttributeError(f"Environment key {name!r} not found") from exc

    def __dir__(self):
        # Show dynamic keys + regular attributes in IDEs
        base = set(super().__dir__())
        return sorted(base | set(self._values.keys()))

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._values.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        return _to_bool(self._values.get(key), default=default)


@dataclass(frozen=True)
class SecretsConfig:
    _values: Dict[str, str]

    def __getattr__(self, name: str) -> Optional[str]:
        try:
            return self._values[name]
        except KeyError as exc:
            raise AttributeError(f"Secret key {name!r} not found") from exc

    def __dir__(self):
        base = set(super().__dir__())
        return sorted(base | set(self._values.keys()))

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._values.get(key, default)


@dataclass(frozen=True)
class Config:
    profile: str
    env: EnvConfig
    secrets: SecretsConfig


@lru_cache(maxsize=None)
def load_config(profile: Optional[str] = None) -> Config:
    parser = argparse.ArgumentParser(description="Create an enrolment via UI and return credentials.")
    parser.add_argument("--env", default="dev15", help="ENV_PROFILE; default uses ENV_PROFILE or 'dev15'")
    args = parser.parse_args()    

    resolved_profile = _resolve_profile(profile)
    env_file = ENV_DIR / f".env.{resolved_profile}"

    if not env_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {env_file}\n"
            f"Expected files in {ENV_DIR} like .env.dev15, .env.tst1, .env.tst2, .env.preprod"
        )

    # ---- env values ----
    raw_env = dotenv_values(env_file)
    env_values: Dict[str, str] = {
        k: str(v) for k, v in raw_env.items() if v is not None
    }
    env_cfg = EnvConfig(env_values)

    # ---- secrets (common + env-specific) ----
    secrets_values: Dict[str, str] = {}

    common_secrets = SECRETS_DIR / ".secrets"
    env_secrets = SECRETS_DIR / f".secrets.{resolved_profile}"

    if common_secrets.exists():
        raw_common = dotenv_values(common_secrets)
        secrets_values.update({k: str(v) for k, v in raw_common.items() if v is not None})

    if env_secrets.exists():
        raw_env_specific = dotenv_values(env_secrets)
        # env-specific overrides common
        secrets_values.update({k: str(v) for k, v in raw_env_specific.items() if v is not None})

    secrets_cfg = SecretsConfig(secrets_values)

    return Config(
        profile=resolved_profile,
        env=env_cfg,
        secrets=secrets_cfg,
    )
