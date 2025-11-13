import os
from dotenv import load_dotenv, dotenv_values
from src.eprda.utils.csv_factory import PROJECT_ROOT


class EnvConfig:
    """
    Unified configuration handler for environment and secret values.

    This class:
      - Loads environment-specific .env files (e.g., .env.dev15)
      - Loads sensitive credentials from a .secrets file
      - Provides unified access to both environment variables and secrets
    """

    # Default environment (can be overridden by ENV system variable)
    ENV = os.getenv("ENV", "dev15")

    def __init__(self):
        # Load environment variables and secrets during initialization
        self._load_env()
        self._load_secrets()

    def _load_env(self):
        """
        Loads environment variables from the .env file
        corresponding to the selected environment.
        Example: config/environments/.env.dev15
        """
        env_file = f"config/environments/.env.{self.ENV}"

        # Ensure the environment file exists before loading
        if not os.path.isfile(env_file):
            raise FileNotFoundError(f"Missing environment file: {env_file}")

        # Load variables into the process environment
        load_dotenv(env_file)
        print(f"✅ Loaded environment: {self.ENV}")

    def _load_secrets(self):
        """
        Loads sensitive credentials from the .secrets file.
        Example: config/credentials/.secrets
        """
        secrets_file = PROJECT_ROOT / "config" / "secrets" / ".secrets"

        # Ensure the secrets file exists before loading
        if not secrets_file.exists():
            raise FileNotFoundError(f"Missing secrets file: {secrets_file}")

        # Read and clean up all key-value pairs
        self._secrets = {
            k: self._clean(v)
            for k, v in dotenv_values(secrets_file).items()
        }

        # Optionally, attach secrets as attributes for direct access (e.g., config.ISSUER)
        self.__dict__.update(self._secrets)

    @staticmethod
    def _clean(value):
        """
        Strips whitespace and surrounding quotes from a value.
        Ensures clean and consistent formatting.
        """
        return value.strip().strip('"').strip("'") if value else None

    def getConfig(self, key: str) -> str:
        """
        Retrieves a configuration value.

        - Checks environment variables first (from .env)
        - Falls back to secrets if not found
        - Raises KeyError if the key does not exist
        """
        value = os.getenv(key) or self._secrets.get(key)
        if value is None:
            raise KeyError(f"Missing key: {key}")
        return value

    def all(self) -> dict:
        """
        Returns all loaded secrets as a dictionary.
        Useful for debugging or inspection (avoid printing in production).
        """
        return self._secrets
