"""DataDog service module for handling DataDog API interactions."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from app.helpers.secrets_service import SecretsService
from sqlalchemy.orm import Session

import requests
from fastapi.responses import JSONResponse
from app.models import DatadogAPIConfiguration

logger = logging.getLogger(__name__)


class DatadogService:
    def __init__(self, user_id: int, db: Session):
        config = (
            db.query(DatadogAPIConfiguration)
            .filter(DatadogAPIConfiguration.user_id == user_id)
            .first()
        )
        secrets = SecretsService()
        self.app_key = secrets.get_customer_secret(config.app_key)
        self.api_key = secrets.get_customer_secret(config.api_key)
        self.base_url = "https://api.datadoghq.com/api/v1"

    def get_monthly_costs(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Get monthly costs from Datadog API
        start_date and end_date format: YYYY-MM
        """
        if not start_date:
            now = datetime.utcnow()
            start_date = (now - timedelta(days=365)).strftime("%Y-%m")
        if not end_date:
            end_date = datetime.utcnow().strftime("%Y-%m")

        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }

        try:
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
                                "month": date.strftime("%m-%Y"),
                                "cost": round(
                                    float(entry["attributes"]["total_cost"]), 2
                                ),
                            }
                        )
                return {"data": monthly_costs}

            if response.status_code == 403:
                logger.error("Datadog API authorization failed")
                raise Exception("Datadog API authorization failed")

            logger.error(
                f"Datadog API request failed with status {response.status_code}"
            )
            raise Exception(f"Failed to retrieve Datadog costs: {response.text}")

        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise Exception(f"Failed to retrieve Datadog costs: {str(e)}")
