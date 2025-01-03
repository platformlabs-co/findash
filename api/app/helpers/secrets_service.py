from infisical_sdk import InfisicalSDKClient
from typing import Optional
import json
from app.helpers.config import Config


class SecretsService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecretsService, cls).__new__(cls)

            config = Config()

            cls._env = config.Environment

            client_id = config.InfisicalClientId
            client_secret = config.InfisicalClientSecret
            project_id = config.InfisicalProjectId

            if not all([client_id, client_secret, project_id]):
                raise ValueError(
                    "INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET, INFISICAL_PROJECT_ID must be set"
                )

            try:
                client = InfisicalSDKClient(host="https://app.infisical.com")
                client.auth.universal_auth.login(
                    client_id=client_id, client_secret=client_secret
                )
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
                environment_slug=self._env,
                secret_path=secret_path,
            )
            return secret.to_dict()["secret"]["secretValue"]
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return default

    def create_customer_secret(
        self, secret_name: str, secret_value: str | dict, secret_type: str
    ) -> str:
        """
        Create or update a customer secret in Infisical.
        If secret_value is a dict, it will be stored as JSON.
        """
        if isinstance(secret_value, dict):
            secret_value = json.dumps(secret_value)

        try:
            self._client.secrets.create_secret_by_name(
                secret_name=secret_name,
                project_id=self._project_id,
                secret_path="/customer-secrets",
                environment_slug=self._env,
                secret_value=secret_value,
            )
        # If secret already exists we update
        except Exception:
            self._client.secrets.update_secret_by_name(
                current_secret_name=secret_name,
                project_id=self._project_id,
                secret_path="/customer-secrets",
                environment_slug=self._env,
                secret_value=secret_value,
            )
        return secret_name

    def get_customer_secret(self, secret_id: str) -> str | dict:
        """
        Retrieve a customer secret from Infisical.
        If the value is JSON, it will be parsed into a dict.
        """
        value = self.get_secret(secret_name=secret_id, secret_path="/customer-secrets")
        if not value:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
