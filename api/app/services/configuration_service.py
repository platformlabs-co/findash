from sqlalchemy.orm import Session
from app.models import User, DatadogAPIConfiguration, AWSAPIConfiguration
from fastapi import HTTPException
from app.helpers.secrets_service import SecretsService


class ConfigurationService:
    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
        self.secrets = SecretsService()

    def _configure_datadog(self, secrets_data: dict) -> tuple[int, str]:
        app_key = self.secrets.create_customer_secret(
            f"user_{self.user.sub}_datadog_app_key",
            secrets_data["DATADOG_APP_KEY"],
            "datadog",
        )
        api_key = self.secrets.create_customer_secret(
            f"user_{self.user.sub}_datadog_api_key",
            secrets_data["DATADOG_API_KEY"],
            "datadog",
        )
        secret = DatadogAPIConfiguration(
            user_id=self.user.id, app_key=app_key, api_key=api_key
        )
        # Check if config already exists for this user
        existing_config = (
            self.db.query(DatadogAPIConfiguration)
            .filter(
                DatadogAPIConfiguration.user_id == self.user.id,
            )
            .first()
        )

        if existing_config:
            existing_config.app_key = app_key
            existing_config.api_key = api_key
            self.db.commit()
            return existing_config.id, "Datadog configuration updated successfully"
        else:
            self.db.add(secret)
            self.db.commit()
            return secret.id, "Datadog configuration created successfully"

    def _configure_aws(self, secrets_data: dict) -> tuple[int, str]:
        access_key = self.secrets.create_customer_secret(
            f"user_{self.user.sub}_aws_access_key",
            secrets_data["AWS_ACCESS_KEY_ID"],
            "aws",
        )
        secret_key = self.secrets.create_customer_secret(
            f"user_{self.user.sub}_aws_secret_key",
            secrets_data["AWS_SECRET_ACCESS_KEY"],
            "aws",
        )
        secret = AWSAPIConfiguration(
            user_id=self.user.id,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        # Check if config already exists for this user
        existing_config = (
            self.db.query(AWSAPIConfiguration)
            .filter(
                AWSAPIConfiguration.user_id == self.user.id,
            )
            .first()
        )

        if existing_config:
            existing_config.aws_access_key_id = access_key
            existing_config.aws_secret_access_key = secret_key
            self.db.commit()
            return existing_config.id, "AWS configuration updated successfully"
        else:
            self.db.add(secret)
            self.db.commit()
            return secret.id, "AWS configuration created successfully"

    def configure_vendor(self, config_type: str, secrets_data: dict) -> tuple[int, str]:
        """
        Configure a vendor (AWS or Datadog) with the provided secrets.
        Returns (config_id, message)
        """
        try:
            if config_type == "datadog":
                config_id, message = self._configure_datadog(secrets_data)

            elif config_type == "aws":
                config_id, message = self._configure_aws(secrets_data)

            return config_id, message

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
