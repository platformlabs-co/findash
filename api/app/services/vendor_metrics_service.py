from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import VendorMetrics, User, DatadogAPIConfiguration, AWSAPIConfiguration
from app.services.aws_service import AWSService
from app.services.datadog_service import DatadogService
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class VendorMetricsService:
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db

    @classmethod
    async def batch_update_all_vendor_metrics(cls, db: Session) -> Dict[str, List[str]]:
        """Update metrics for all users and their configurations"""
        results: Dict[str, List[str]] = {"success": [], "failed": []}

        try:
            # Get all users with their configurations
            users = db.query(User).all()

            for user in users:
                service = cls(user.id, db)

                # Update AWS metrics for each configuration
                aws_configs = (
                    db.query(AWSAPIConfiguration)
                    .filter(AWSAPIConfiguration.user_id == user.id)
                    .all()
                )

                for config in aws_configs:
                    try:
                        await service.get_and_store_vendor_metrics(
                            "aws", config.identifier
                        )
                        msg = f"AWS metrics updated for user {user.id}, config {config.identifier}"
                        results["success"].append(msg)
                    except Exception as e:
                        error_msg = (
                            f"Failed to update AWS metrics for user {user.id}, "
                            f"config {config.identifier}: {str(e)}"
                        )
                        logger.error(error_msg)
                        results["failed"].append(error_msg)

                # Update Datadog metrics for each configuration
                datadog_configs = (
                    db.query(DatadogAPIConfiguration)
                    .filter(DatadogAPIConfiguration.user_id == user.id)
                    .all()
                )

                for config in datadog_configs:
                    try:
                        await service.get_and_store_vendor_metrics(
                            "datadog", config.identifier
                        )
                        msg = (
                            f"Datadog metrics updated for user {user.id}, "
                            f"config {config.identifier}"
                        )
                        results["success"].append(msg)
                    except Exception as e:
                        error_msg = (
                            f"Failed to update Datadog metrics for user {user.id}, "
                            f"config {config.identifier}: {str(e)}"
                        )
                        logger.error(error_msg)
                        results["failed"].append(error_msg)

        except Exception as e:
            error_msg = f"Batch update failed: {str(e)}"
            logger.error(error_msg)
            results["failed"].append(error_msg)

        return results

    async def get_and_store_vendor_metrics(
        self, vendor: str, identifier: str = "Default Configuration"
    ):
        """Get vendor metrics and store them in the database"""
        try:
            # Get costs from vendor service
            costs = await self._get_vendor_costs(vendor, identifier)

            # Store metrics in database
            self._store_metrics(vendor, identifier, costs["data"])

            return costs
        except Exception as e:
            raise Exception(f"Failed to get and store {vendor} metrics: {str(e)}")

    async def _get_vendor_costs(self, vendor: str, identifier: str):
        """Get costs from the appropriate vendor service"""
        if vendor.lower() == "datadog":
            service = DatadogService(self.user_id, self.db, identifier=identifier)
            return await service.get_monthly_costs()
        elif vendor.lower() == "aws":
            service = AWSService(self.user_id, self.db, identifier=identifier)
            return await service.get_monthly_costs()
        else:
            raise ValueError(f"Unsupported vendor: {vendor}")

    def _store_metrics(self, vendor: str, identifier: str, cost_data: list):
        """Store metrics in the database"""
        for cost_item in cost_data:
            # Check if metric already exists
            existing_metric = (
                self.db.query(VendorMetrics)
                .filter(
                    and_(
                        VendorMetrics.user_id == self.user_id,
                        VendorMetrics.vendor == vendor.lower(),
                        VendorMetrics.identifier == identifier,
                        VendorMetrics.month == cost_item["month"],
                    )
                )
                .first()
            )

            if existing_metric:
                # Update existing metric
                existing_metric.cost = cost_item["cost"]
            else:
                # Create new metric
                metric = VendorMetrics(
                    user_id=self.user_id,
                    vendor=vendor.lower(),
                    identifier=identifier,
                    month=cost_item["month"],
                    cost=cost_item["cost"],
                )
                self.db.add(metric)

        self.db.commit()
