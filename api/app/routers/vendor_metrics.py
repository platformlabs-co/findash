import logging
from datetime import datetime, timedelta
import requests
from typing import Dict, Any

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from pydantic import BaseModel

class DatadogMetricsFetcher:
    def __init__(self, api_key: str, app_key: str):
        self.api_key = api_key
        self.app_key = app_key
        self.base_url = "https://api.datadoghq.com/api/v1"

    def get_usage_data(self) -> Dict[str, Any]:
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
                params={
                    "start_month": start_date,
                    "end_month": end_date
                }
            )
            
            logger.info(f"Datadog API Response - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                monthly_costs = []
                if 'data' in data and isinstance(data['data'], list):
                    for entry in data['data']:
                        date = datetime.strptime(entry['attributes']['date'], "%Y-%m-%d")
                        monthly_costs.append({
                            'month': date.strftime("%m-%Y"),
                            'cost': round(float(entry['attributes']['total_cost']), 2)
                        })
                return {"data": monthly_costs}
            logger.info(f"Datadog API Response - Body: {response.text}")
            
            if response.status_code == 403:
                logger.error("Datadog API authorization failed")
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Authorization failed",
                        "message": "Invalid API key or application key",
                        "details": response.text
                    }
                )
            elif response.status_code != 200:
                logger.error(f"Datadog API request failed with status {response.status_code}")
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "error": "Failed to fetch Datadog metrics",
                        "message": response.text,
                        "status": response.status_code
                    }
                )
            
            logger.info("Successfully retrieved Datadog metrics")
            return response.json()
            
        except requests.RequestException as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Request failed",
                    "message": str(e),
                    "type": type(e).__name__
                }
            )

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
            
        fetcher = DatadogMetricsFetcher(api_key=datadog_config.api_key, app_key=datadog_config.app_key)
        logger.debug("Fetching Datadog usage data")
        metrics = fetcher.get_usage_data()
        
        if isinstance(metrics, JSONResponse):
            return metrics
            
        logger.info("Successfully retrieved Datadog metrics")
        return JSONResponse(
            status_code=200,
            content={
                "data": metrics,
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