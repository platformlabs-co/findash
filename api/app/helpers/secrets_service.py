from infisical import InfisicalClient
import os
import requests
from typing import Optional


class SecretsService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretsService, cls).__new__(cls)
            client_id = os.getenv("INFISICAL_CLIENT_ID")
            client_secret = os.getenv("INFISICAL_CLIENT_SECRET")

            if not client_id or not client_secret:
                raise ValueError(
                    "INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET must be set"
                )

            response = requests.post(
                "https://app.infisical.com/api/v3/auth/oauth/client-credentials",
                json={"clientId": client_id, "clientSecret": client_secret},
            )

            if response.status_code != 200:
                raise Exception("Failed to authenticate with Infisical")

            access_token = response.json()["accessToken"]
            cls._client = InfisicalClient(token=access_token)

        return cls._instance

    def get_secret(
        self, secret_name: str, default: Optional[str] = None
    ) -> Optional[str]:
        try:
            return self._client.get_secret(secret_name).secret_value
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return default
