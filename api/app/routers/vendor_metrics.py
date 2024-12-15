import logging
from datetime import datetime, timedelta
import requests
from typing import Dict, Any

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User, VendorMetric # Added VendorMetric import
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
        start_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        
        headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }
        
        response = requests.get(
            f"{self.base_url}/usage/hosts?start_hr={start_date}&end_hr={end_date}",
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch Datadog metrics: {response.text}"
            )
            
        return response.json()

logger = logging.getLogger(__name__)

class DatadogAPIConfigCreate(BaseModel):
    app_key: str | None = None
    api_key: str | None = None

router = APIRouter(tags=["cloud-cost-data"])

@router.get("/v1/vendors-metrics/{vendor_id}") # Added vendor_id path parameter
async def get_vendor_metrics(vendor_id: int, request: Request, auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)):
    try:
        vendor = db.query(VendorMetric).filter(VendorMetric.id == vendor_id).first()
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        if vendor.type == "datadog":
            config = db.query(DatadogAPIConfiguration).filter(DatadogAPIConfiguration.user_id == auth_user["user_id"]).first()
            if not config:
                raise HTTPException(status_code=404, detail="Datadog configuration not found for this user")
            fetcher = DatadogMetricsFetcher(api_key=config.api_key, app_key=config.app_key)
            metrics = fetcher.get_usage_data()
            return JSONResponse({"data": metrics})
        else:
            raise HTTPException(status_code=400, detail=f"Vendor type '{vendor.type}' not implemented")

    except Exception as e:
        logger.exception(f"Error fetching vendor metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


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

from fastapi.responses import JSONResponse

from app.helpers.auth import get_authenticated_user

logger = logging.getLogger(__name__)


router = APIRouter(tags=["cloud-cost-data"])


@router.get("/v1/vendors-metrics") #This endpoint is redundant and should likely be removed or repurposed
async def home(request: Request, auth_user: dict = Depends(get_authenticated_user)):
    return JSONResponse(
        {"data": {"message": "Welcome to the FinDash API", "user": auth_user}}
    )