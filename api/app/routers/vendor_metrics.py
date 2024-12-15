import logging

from fastapi import APIRouter, Request, Depends

import logging

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DatadogAPIConfigCreate(BaseModel):
    app_key: str | None = None
    api_key: str | None = None

router = APIRouter(tags=["cloud-cost-data"])

@router.get("/v1/vendors-metrics")
async def home(request: Request, auth_user: dict = Depends(get_authenticated_user)):
    return JSONResponse(
        {"data": {"message": "Welcome to the FinDash API", "user": auth_user}}
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


@router.get("/v1/vendors-metrics")
async def home(request: Request, auth_user: dict = Depends(get_authenticated_user)):
    return JSONResponse(
        {"data": {"message": "Welcome to the FinDash API", "user": auth_user}}
    )
