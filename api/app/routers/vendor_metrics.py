import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.services.datadog_service import DatadogService
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DatadogAPIConfigCreate(BaseModel):
    app_key: str | None = None
    api_key: str | None = None

router = APIRouter(tags=["cloud-cost-data"])

@router.get("/v1/vendors-metrics/{vendor_name}")
async def get_vendor_metrics(vendor_name: str, request: Request, auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching metrics for vendor: {vendor_name}, user_sub: {auth_user['sub']}")
        user = db.query(User).filter(User.sub == auth_user["sub"]).first()
        if not user:
            logger.error(f"User not found for sub: {auth_user['sub']}")
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

        logger.info("Processing Datadog metrics request")
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
        logger.debug("Fetching Datadog usage data")
        metrics = service.get_historical_data()
        
        if isinstance(metrics, JSONResponse):
            return metrics
            
        logger.info("Successfully retrieved Datadog metrics")
        # Calculate total sum
        total_sum = sum(entry['cost'] for entry in metrics['data']) if metrics.get('data') else 0
        
        return JSONResponse(
            status_code=200,
            content={
                **metrics,
                "total_sum": total_sum,
                "message": "Successfully retrieved metrics"
            }
        )

    except Exception as e:
        logger.exception(f"Error fetching vendor metrics: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e),
                "code": "INTERNAL_ERROR"
            }
        )


@router.post("/v1/datadog-configuration")
async def create_datadog_configuration(
    config: DatadogAPIConfigCreate,
    auth_user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db)
):
    if not config.app_key and not config.api_key:
        raise HTTPException(
            status_code=400, 
            detail="At least one of app_key or api_key must be provided"
        )
        
    # Get user ID from database
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for existing configuration
    existing_config = db.query(DatadogAPIConfiguration).filter(
        DatadogAPIConfiguration.user_id == user.id
    ).first()
    
    if existing_config:
        # Update existing configuration
        existing_config.app_key = config.app_key if config.app_key else existing_config.app_key
        existing_config.api_key = config.api_key if config.api_key else existing_config.api_key
        api_config = existing_config
    else:
        # Create new configuration
        api_config = DatadogAPIConfiguration(
            user_id=user.id,
            app_key=config.app_key,
            api_key=config.api_key
        )
        db.add(api_config)
    
    db.commit()
    db.refresh(api_config)
    
    return JSONResponse({
        "data": {
            "message": "Datadog API configuration created successfully",
            "id": api_config.id
        }
    })