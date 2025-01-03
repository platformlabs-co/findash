from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
from ..helpers.secrets_service import SecretsService
from sqlalchemy.orm import Session
from app.models import AWSAPIConfiguration


class AWSService:
    def __init__(self, user_id: int, db: Session):
        config = (
            db.query(AWSAPIConfiguration)
            .filter(AWSAPIConfiguration.user_id == user_id)
            .first()
        )
        secrets = SecretsService()
        self.client = boto3.client(
            "ce",  # Cost Explorer
            aws_access_key_id=secrets.get_customer_secret(config.aws_access_key_id),
            aws_secret_access_key=secrets.get_customer_secret(
                config.aws_secret_access_key
            ),
            region_name="us-east-1",  # default region for CE
        )

    async def get_monthly_costs(self):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)  # Last 12 months

            response = self.client.get_cost_and_usage(
                TimePeriod={
                    "Start": start_date.strftime("%Y-%m-01"),
                    "End": end_date.strftime("%Y-%m-%d"),
                },
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
            )

            # Transform the data to match Datadog format
            monthly_costs = []
            for time_period in response.get("ResultsByTime", []):
                period_start = datetime.strptime(
                    time_period["TimePeriod"]["Start"], "%Y-%m-%d"
                )
                month = period_start.strftime("%B %Y")

                total_cost = sum(
                    float(group["Metrics"]["UnblendedCost"]["Amount"])
                    for group in time_period["Groups"]
                )

                monthly_costs.append({"month": month, "cost": round(total_cost, 2)})

            return {
                "data": monthly_costs,
                "message": "Successfully retrieved AWS monthly costs",
            }

        except ClientError as e:
            raise Exception(f"Failed to retrieve AWS costs: {str(e)}")
