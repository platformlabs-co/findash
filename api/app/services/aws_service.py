from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
from ..helpers.secrets_service import SecretsService
from sqlalchemy.orm import Session
from app.models import AWSAPIConfiguration
import logging

logger = logging.getLogger(__name__)


class AWSService:
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
        self.secrets = SecretsService()
        self._init_client()

    def _init_client(self):
        config = (
            self.db.query(AWSAPIConfiguration)
            .filter(AWSAPIConfiguration.user_id == self.user_id)
            .first()
        )
        if not config:
            raise Exception("AWS configuration not found")

        access_key = self.secrets.get_customer_secret(config.aws_access_key_id)
        secret_key = self.secrets.get_customer_secret(config.aws_secret_access_key)

        if not access_key or not secret_key:
            raise Exception("AWS credentials not found")

        logger.info(
            f"AWS credentials found for user {self.user_id} {access_key} {secret_key}"
        )

        self.client = boto3.client(
            "ce",  # Cost Explorer service
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",  # Cost Explorer is available in us-east-1
        )

    def get_monthly_costs(self):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)  # Last 12 months

            response = self.client.get_cost_and_usage(
                TimePeriod={
                    "Start": start_date.strftime("%Y-%m-%d"),
                    "End": end_date.strftime("%Y-%m-%d"),
                },
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
            )

            cost_data = []
            for result in response["ResultsByTime"]:
                month = datetime.strptime(
                    result["TimePeriod"]["Start"], "%Y-%m-%d"
                ).strftime("%m-%Y")
                cost = float(result["Total"]["UnblendedCost"]["Amount"])
                cost_data.append(
                    {
                        "month": month,
                        "cost": round(cost, 2),
                    }
                )

            return {"data": cost_data}

        except ClientError as e:
            logger.error(f"AWS API error: {str(e)}")
            raise Exception(f"Failed to retrieve AWS costs: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching AWS costs: {str(e)}")
            raise Exception(f"Failed to retrieve AWS costs: {str(e)}")
