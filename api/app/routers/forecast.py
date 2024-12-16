import logging
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
import io
import csv
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.services.datadog_service import DatadogService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["cloud-cost-forecast"])


@router.get("/v1/vendors-forecast/{vendor_name}")
async def get_vendor_forecast(
    vendor_name: str,
    format: str = Query(None, description="Response format (csv or json)"),
    auth_user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    try:
        user = db.query(User).filter(User.sub == auth_user["sub"]).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "User not found",
                    "message": "Unable to find user record",
                    "code": "USER_NOT_FOUND",
                },
            )

        vendor_name = vendor_name.lower()
        if vendor_name != "datadog":
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid vendor",
                    "message": f"Vendor type '{vendor_name}' not implemented",
                    "code": "INVALID_VENDOR",
                },
            )

        datadog_config = (
            db.query(DatadogAPIConfiguration)
            .filter(DatadogAPIConfiguration.user_id == user.id)
            .first()
        )

        if not datadog_config:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "Configuration not found",
                    "message": "Datadog API configuration not found for this user",
                    "code": "CONFIG_NOT_FOUND",
                },
            )

        service = DatadogService(
            api_key=datadog_config.api_key, app_key=datadog_config.app_key
        )
        historical_data = service.get_historical_data()

        if isinstance(historical_data, JSONResponse):
            return historical_data

        from app.services.forecast_service import ForecastService

        # Generate forecast using the ForecastService
        forecast_data = ForecastService.predict_mom_growth(historical_data["data"])

        if format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)

            # Write headers
            writer.writerow(
                ["Month", "Best Case", "Trend-based Forecast", "Worst Case"]
            )

            # Write forecast data
            for entry in forecast_data["forecast_data"]:
                writer.writerow(
                    [
                        entry["month"],
                        entry["best_case"],
                        entry["cost"],
                        entry["worst_case"],
                    ]
                )

            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename={vendor_name}_forecast.csv"
                },
            )

        return JSONResponse(
            status_code=200,
            content={
                "historical": historical_data["data"],
                "forecast": forecast_data["forecast_data"],
                "sums": forecast_data["sums"],
                "growth_rates": forecast_data["growth_rates"],
                "message": "Successfully retrieved forecast",
            },
        )

    except Exception as e:
        logger.error(f"Error in forecast: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e),
                "code": "INTERNAL_ERROR",
            },
        )
