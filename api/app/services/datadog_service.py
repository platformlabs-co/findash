"""DataDog service module for handling DataDog API interactions."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from app.helpers.secrets_service import SecretsService

import requests
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class DatadogService:
    def __init__(self, app_key_secret_id: str, api_key_secret_id: str):
        secrets = SecretsService()
        self.app_key = (
            secrets._client.get_secret_by_id(app_key_secret_id).secret_value
            if app_key_secret_id
            else None
        )
        self.api_key = (
            secrets._client.get_secret_by_id(api_key_secret_id).secret_value
            if api_key_secret_id
            else None
        )
        self.base_url = "https://api.datadoghq.com/api/v1"

    def get_historical_data(self) -> Dict[str, Any]:
        now = datetime.utcnow()
        start_date = (now - timedelta(days=365)).strftime("%Y-%m")
        end_date = now.strftime("%Y-%m")

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
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Authorization failed",
                        "message": "Invalid API key or application key",
                        "details": response.text,
                    },
                )

            logger.error(
                f"Datadog API request failed with status {response.status_code}"
            )
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "error": "Failed to fetch Datadog metrics",
                    "message": response.text,
                    "status": response.status_code,
                },
            )

        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Request failed",
                    "message": str(e),
                    "type": type(e).__name__,
                },
            )
