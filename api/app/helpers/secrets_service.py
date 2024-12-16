from infisical_sdk import InfisicalSDKClient
import os
from typing import Optional


class SecretsService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretsService, cls).__new__(cls)
            client_id = os.getenv("INFISICAL_CLIENT_ID")
            client_secret = os.getenv("INFISICAL_CLIENT_SECRET")
            project_id = os.getenv("INFISICAL_PROJECT_ID")
        
            if not all([client_id, client_secret, project_id]):
                raise ValueError(
                    "INFISICAL_CLIENT_ID, INFISICAL_CLIENT_SECRET and INFISICAL_PROJECT_ID must be set"
                )

            try:
                client = InfisicalSDKClient(host="https://app.infisical.com")
                client.auth.universal_auth.login(client_id=client_id, client_secret=client_secret)
                cls._client = client
                cls._project_id = project_id
            except Exception as e:
                raise Exception(f"Failed to authenticate with Infisical: {str(e)}")

        return cls._instance

    def get_secret(
        self, secret_name: str, default: Optional[str] = None
    ) -> Optional[str]:
        try:
            secrets = self._client.secrets.listSecrets(
                project_id=self._project_id, 
                environment_slug="dev", 
                secret_path="/"
            )
            for secret in secrets:
                if secret.secret_name == secret_name:
                    return secret.secret_value
            return default
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return default
