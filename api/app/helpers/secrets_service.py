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
            project_id = "e2285640-9115-45c6-9888-e7427b3f8c0a"
        
            if not all([client_id, client_secret]):
                raise ValueError(
                    "INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET must be set"
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
        self, secret_name: str, default: Optional[str] = None, secret_path: str = "/"
    ) -> Optional[str]:
        try:
            secret = self._client.secrets.get_secret_by_name(
                secret_name=secret_name,
                project_id=self._project_id,
                environment_slug="dev",
                secret_path=secret_path,
            )
            print(secret.to_dict()["secret"])
            return secret.to_dict()["secret"]["secretValue"]
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return default

    def create_customer_secret(
        self, secret_name: str, secret_value: str, tag: Optional[str] = None
    ):
        try:
            secret = self._client.secrets.create_secret_by_name(
                secret_name=secret_name,
                project_id=self._project_id,
                secret_path="/customer-secrets",
                environment_slug="dev",
                secret_value=secret_value,
            )
        # If secret already exists we update
        except Exception as e:
            secret = self._client.secrets.update_secret_by_name(
                current_secret_name=secret_name,
                project_id=self._project_id,
                secret_path="/customer-secrets",
                environment_slug="dev",
                secret_value=secret_value,
            )
        return secret_name

