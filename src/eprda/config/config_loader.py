import os
from pathlib import Path
from dotenv import dotenv_values, load_dotenv
# Project root: go up from src/eprda/config to find project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Directory where .env files live
ENV_DIR = PROJECT_ROOT / "config" / "environments"


def load_env(profile: str | None = None) -> str:
    """
    Load environment variables from:
        config/environments/.env.<profile>

    - profile comes from ENV_PROFILE env var
    - defaults to 'dev15'
    - example files:
        .env.dev15
        .env.tst1
        .env.tst2

    Returns:
        The resolved profile name (str)
    """
    # Determine profile
    profile = profile or os.getenv("ENV_PROFILE", "dev15")
    profile = profile.strip()

    # Resolve file path
    env_file = ENV_DIR / f".env.{profile}"

    if not env_file.exists():
        raise FileNotFoundError(
            f"❌ Environment file not found: {env_file}\n"
            f"Make sure the file exists under config/environments/"
        )

    # Load .env file
    load_dotenv(env_file, override=True)
    print(f"✅ Loaded environment: {env_file}")

    return profile


def get_bool(name: str, default: bool) -> bool:
    """Parse an environment variable as a boolean."""
    v = os.getenv(name, str(default)).strip().lower()
    return v in ("1", "true", "yes", "on")


class Settings:
    """Centralized settings for automation."""

    def __init__(self):
        self.producer_base_url = os.getenv("PRODUCER_BASE_URL")
        self.regulator_base_url = os.getenv("REGULATOR_BASE_URL")
        self.headless = get_bool("HEADLESS", True)

        if not self.producer_base_url:
            raise EnvironmentError(
                "❌ PRODUCER_BASE_URL not set — missing or incorrect .env file."
            )

    def __repr__(self):
        return (
            f"<Settings producer_base_url={self.producer_base_url}, "
            f"regulator_base_url={self.regulator_base_url}, "
            f"headless={self.headless}>"
        )

class Secrets:
    _secrets_path = PROJECT_ROOT / "config" / "credentials" / ".secrets"
    _secrets = dotenv_values(dotenv_path=_secrets_path)

    def __init__(self):
        self.ISSUER = self._clean_value(Secrets._secrets.get("ISSUER"))
        self.SECRET = self._clean_value(Secrets._secrets.get("SECRET"))
        self.COMPANY_HOUSE_TOKEN = self._clean_value(Secrets._secrets.get("COMPANY_HOUSE_TOKEN"))

    def _clean_value(self, value):
        if value is None:
            return None
        return value.strip().strip('"').strip("'")

    def all(self):
        return {k: self._clean_value(v) for k, v in Secrets._secrets.items()}
