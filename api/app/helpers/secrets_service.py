
from infisical import InfisicalClient
import os

class SecretsService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretsService, cls).__new__(cls)
            cls._client = InfisicalClient(token=os.getenv("INFISICAL_TOKEN"))
        return cls._instance

    def get_secret(self, secret_name: str, default: str = None) -> str:
        try:
            return self._client.get_secret(secret_name).secret_value
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return default
