import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.vendor_metrics_service import VendorMetricsService
from app.models import VendorMetrics, User, AWSAPIConfiguration, DatadogAPIConfiguration


@pytest.fixture
def mock_db():
    db = Mock()
    # Setup query.all() to return an empty list by default
    db.query.return_value.all.return_value = []
    return db


@pytest.fixture
def mock_user():
    user = Mock(spec=User)
    user.id = 1
    return user


@pytest.fixture
def mock_aws_config():
    config = Mock(spec=AWSAPIConfiguration)
    config.identifier = "test-aws"
    return config


@pytest.fixture
def mock_datadog_config():
    config = Mock(spec=DatadogAPIConfiguration)
    config.identifier = "test-datadog"
    return config


@pytest.fixture
def mock_costs_response():
    return {
        "data": [
            {"month": "01-2024", "cost": 100.0},
            {"month": "02-2024", "cost": 200.0},
        ]
    }


class TestVendorMetricsService:
    @pytest.mark.asyncio
    async def test_get_and_store_vendor_metrics_aws_success(
        self, mock_db, mock_user, mock_costs_response
    ):
        """
        GIVEN a VendorMetricsService instance and AWS vendor
        WHEN get_and_store_vendor_metrics is called
        THEN it should fetch costs and store them in the database
        """
        # GIVEN
        service = VendorMetricsService(mock_user.id, mock_db)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with patch(
            "app.services.vendor_metrics_service.AWSService",
            autospec=True,
        ) as mock_aws_service:
            mock_aws_instance = Mock()
            mock_aws_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_aws_service.return_value = mock_aws_instance

            # WHEN
            result = await service.get_and_store_vendor_metrics("aws", "test-config")

            # THEN
            assert result == mock_costs_response
            assert mock_db.add.call_count == 2  # Two months of data
            mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_and_store_vendor_metrics_datadog_success(
        self, mock_db, mock_user, mock_costs_response
    ):
        """
        GIVEN a VendorMetricsService instance and Datadog vendor
        WHEN get_and_store_vendor_metrics is called
        THEN it should fetch costs and store them in the database
        """
        # GIVEN
        service = VendorMetricsService(mock_user.id, mock_db)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with patch(
            "app.services.vendor_metrics_service.DatadogService",
            autospec=True,
        ) as mock_dd_service:
            mock_dd_instance = Mock()
            mock_dd_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_dd_service.return_value = mock_dd_instance

            # WHEN
            result = await service.get_and_store_vendor_metrics(
                "datadog", "test-config"
            )

            # THEN
            assert result == mock_costs_response
            assert mock_db.add.call_count == 2  # Two months of data
            mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_and_store_vendor_metrics_update_existing(
        self, mock_db, mock_user, mock_costs_response
    ):
        """
        GIVEN a VendorMetricsService instance and existing metrics
        WHEN get_and_store_vendor_metrics is called
        THEN it should update existing metrics instead of creating new ones
        """
        # GIVEN
        service = VendorMetricsService(mock_user.id, mock_db)
        existing_metric = Mock(spec=VendorMetrics)
        mock_db.query.return_value.filter.return_value.first.return_value = (
            existing_metric
        )

        with patch(
            "app.services.vendor_metrics_service.AWSService",
            autospec=True,
        ) as mock_aws_service:
            mock_aws_instance = Mock()
            mock_aws_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_aws_service.return_value = mock_aws_instance

            # WHEN
            result = await service.get_and_store_vendor_metrics("aws", "test-config")

            # THEN
            assert result == mock_costs_response
            mock_db.add.assert_not_called()  # Should not add new records
            mock_db.commit.assert_called_once()
            assert existing_metric.cost == mock_costs_response["data"][1]["cost"]

    @pytest.mark.asyncio
    async def test_get_and_store_vendor_metrics_invalid_vendor(
        self, mock_db, mock_user
    ):
        """
        GIVEN a VendorMetricsService instance
        WHEN get_and_store_vendor_metrics is called with invalid vendor
        THEN it should raise ValueError
        """
        # GIVEN
        service = VendorMetricsService(mock_user.id, mock_db)

        # WHEN/THEN
        with pytest.raises(ValueError, match="Unsupported vendor: invalid"):
            await service.get_and_store_vendor_metrics("invalid", "test-config")

    @pytest.mark.asyncio
    async def test_batch_update_all_vendor_metrics_success(
        self,
        mock_db,
        mock_user,
        mock_aws_config,
        mock_datadog_config,
        mock_costs_response,
    ):
        """
        GIVEN a database with users and their configurations
        WHEN batch_update_all_vendor_metrics is called
        THEN it should update metrics for all users and configurations
        """
        # GIVEN
        mock_db.query.return_value.all.side_effect = [
            [mock_user],  # Users query
        ]
        mock_db.query.return_value.filter.return_value.all.side_effect = [
            [mock_aws_config],  # AWS configs query
            [mock_datadog_config],  # Datadog configs query
        ]

        with patch(
            "app.services.vendor_metrics_service.AWSService",
            autospec=True,
        ) as mock_aws_service, patch(
            "app.services.vendor_metrics_service.DatadogService",
            autospec=True,
        ) as mock_dd_service:
            mock_aws_instance = Mock()
            mock_aws_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_aws_service.return_value = mock_aws_instance

            mock_dd_instance = Mock()
            mock_dd_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_dd_service.return_value = mock_dd_instance

            # Reset mock for storing metrics
            mock_db.query.return_value.filter.return_value.first.return_value = None

            # WHEN
            results = await VendorMetricsService.batch_update_all_vendor_metrics(
                mock_db
            )

            # THEN
            assert len(results["success"]) == 2  # One success message for each config
            assert len(results["failed"]) == 0
            assert any("AWS metrics updated" in msg for msg in results["success"])
            assert any("Datadog metrics updated" in msg for msg in results["success"])

    @pytest.mark.asyncio
    async def test_batch_update_all_vendor_metrics_partial_failure(
        self,
        mock_db,
        mock_user,
        mock_aws_config,
        mock_datadog_config,
        mock_costs_response,
    ):
        """
        GIVEN a database with users and their configurations
        WHEN batch_update_all_vendor_metrics is called and some updates fail
        THEN it should handle errors gracefully and continue processing
        """
        # GIVEN
        mock_db.query.return_value.all.side_effect = [
            [mock_user],  # Users query
        ]
        mock_db.query.return_value.filter.return_value.all.side_effect = [
            [mock_aws_config],  # AWS configs query
            [mock_datadog_config],  # Datadog configs query
        ]

        with patch(
            "app.services.vendor_metrics_service.AWSService",
            autospec=True,
        ) as mock_aws_service, patch(
            "app.services.vendor_metrics_service.DatadogService",
            autospec=True,
        ) as mock_dd_service:
            # AWS service succeeds
            mock_aws_instance = Mock()
            mock_aws_instance.get_monthly_costs = AsyncMock(
                return_value=mock_costs_response
            )
            mock_aws_service.return_value = mock_aws_instance

            # Datadog service fails
            mock_dd_instance = Mock()
            mock_dd_instance.get_monthly_costs = AsyncMock(
                side_effect=Exception("Datadog API error")
            )
            mock_dd_service.return_value = mock_dd_instance

            # Reset mock for storing metrics
            mock_db.query.return_value.filter.return_value.first.return_value = None

            # WHEN
            results = await VendorMetricsService.batch_update_all_vendor_metrics(
                mock_db
            )

            # THEN
            assert len(results["success"]) == 1  # AWS update succeeded
            assert len(results["failed"]) == 1  # Datadog update failed
            assert any("AWS metrics updated" in msg for msg in results["success"])
            assert any(
                "Failed to update Datadog metrics" in msg for msg in results["failed"]
            )
