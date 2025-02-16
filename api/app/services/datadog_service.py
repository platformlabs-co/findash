"""DataDog service module for handling DataDog API interactions."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from app.helpers.secrets_service import SecretsService
from sqlalchemy.orm import Session
import requests
from app.models import DatadogAPIConfiguration

logger = logging.getLogger(__name__)


class DatadogService:
    def __init__(
        self, user_id: int, db: Session, identifier: str = "Default Configuration"
    ):
        config = (
            db.query(DatadogAPIConfiguration)
            .filter(DatadogAPIConfiguration.user_id == user_id)
            .filter(DatadogAPIConfiguration.identifier == identifier)
            .first()
        )
        secrets = SecretsService()
        self.app_key = secrets.get_customer_secret(config.app_key)
        self.api_key = secrets.get_customer_secret(config.api_key)
        self.base_url = "https://api.datadoghq.com/api/v1"

    def get_monthly_costs(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> Dict[str, Any]:
        """
        Get monthly costs from Datadog API
        start_date and end_date format: MM-YYYY
        """
        try:
            # Handle end_date
            if end_date:
                # Convert MM-YYYY to YYYY-MM
                month, year = end_date.split("-")
                end_date = f"{year}-{month}"
            else:
                end_date = datetime.utcnow().strftime("%Y-%m")

            # Handle start_date
            if start_date:
                # Convert MM-YYYY to YYYY-MM
                month, year = start_date.split("-")
                start_date = f"{year}-{month}"
            else:
                # Default to 1 year ago
                start_date = (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m")

            headers = {
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
            }

            response = requests.get(
                "https://api.datadoghq.com/api/v2/usage/historical_cost",
                headers=headers,
                params={"start_month": start_date, "end_month": end_date},
            )

            logger.info(f"Datadog API Response - Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                monthly_costs = []
                if "data" in data and isinstance(data["data"], list):
                    for entry in data["data"]:
                        date = datetime.strptime(
                            entry["attributes"]["date"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                        monthly_costs.append(
                            {
                                "month": date.strftime(
                                    "%m-%Y"
                                ),  # Convert back to MM-YYYY for consistency
                                "cost": round(
                                    float(entry["attributes"]["total_cost"]), 2
                                ),
                            }
                        )
                return {"data": monthly_costs}
            else:
                error_msg = (
                    response.json()
                    if response.content
                    else "No error details available"
                )
                logger.error(f"Datadog API error: {error_msg}")
                raise Exception(f"Failed to retrieve Datadog costs: {error_msg}")

        except Exception as e:
            logger.error(f"Error fetching Datadog costs: {str(e)}")
            raise Exception(f"Failed to retrieve Datadog costs: {str(e)}")
