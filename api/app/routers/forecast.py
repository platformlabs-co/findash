
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
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
    auth_user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.sub == auth_user["sub"]).first()
        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "User not found",
                    "message": "Unable to find user record",
                    "code": "USER_NOT_FOUND"
                }
            )

        vendor_name = vendor_name.lower()
        if vendor_name != "datadog":
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid vendor",
                    "message": f"Vendor type '{vendor_name}' not implemented",
                    "code": "INVALID_VENDOR"
                }
            )

        datadog_config = db.query(DatadogAPIConfiguration).filter(
            DatadogAPIConfiguration.user_id == user.id
        ).first()
        
        if not datadog_config:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "Configuration not found",
                    "message": "Datadog API configuration not found for this user",
                    "code": "CONFIG_NOT_FOUND"
                }
            )

        service = DatadogService(api_key=datadog_config.api_key, app_key=datadog_config.app_key)
        historical_data = service.get_historical_data()
        
        if isinstance(historical_data, JSONResponse):
            return historical_data
            
        # For now, return historical data with zero forecast
        current_date = datetime.now()
        forecast_data = []
        
        for i in range(12):
            future_date = current_date + timedelta(days=30 * (i + 1))
            forecast_data.append({
                'month': future_date.strftime("%m-%Y"),
                'predicted_cost': 0.00
            })
            
        return JSONResponse(
            status_code=200,
            content={
                "historical": historical_data["data"],
                "forecast": forecast_data,
                "message": "Successfully retrieved forecast"
            }
        )

    except Exception as e:
        logger.error(f"Error in forecast: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e),
                "code": "INTERNAL_ERROR"
            }
        )
