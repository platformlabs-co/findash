import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import DatadogAPIConfiguration, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.helpers.secrets_service import SecretsService
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DatadogAPIConfigCreate(BaseModel):
    app_key: str | None = None
    api_key: str | None = None


router = APIRouter(tags=["users"])


@router.post("/v1/users/me/datadog-configuration")
async def create_datadog_configuration(
    config: DatadogAPIConfigCreate,
    auth_user: dict = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    if not config.app_key and not config.api_key:
        raise HTTPException(
            status_code=400,
            detail="At least one of app_key or api_key must be provided",
        )

    # Get user ID from database
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secrets = SecretsService()

    app_key_secret_id = None
    api_key_secret_id = None

    if config.app_key:
        app_key_secret_id = secrets.create_customer_secret(
            f"user_{user.id}_datadog_app_key", config.app_key, "datadog"
        )

    if config.api_key:
        api_key_secret_id = secrets.create_customer_secret(
            f"user_{user.id}_datadog_api_key", config.api_key, "datadog"
        )    
        
    # Create new configuration
    api_config = DatadogAPIConfiguration(
        user_id=user.id,
        app_key_secret_id=app_key_secret_id,
        api_key_secret_id=api_key_secret_id,
    )

    db.add(api_config)
    db.commit()
    db.refresh(api_config)

    return JSONResponse(
        {
            "data": {
                "message": "Datadog API configuration created successfully",
                "id": api_config.id,
            }
        }
    )


@router.get("/v1/users/me/api-configurations")
async def list_api_configurations(
    auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
):
    logger.debug(f"Attempting to fetch configurations for user sub: {auth_user['sub']}")
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        logger.debug(f"User not found for sub: {auth_user['sub']}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.debug(f"Found user with ID: {user.id}")

    configurations = (
        db.query(DatadogAPIConfiguration)
        .filter(DatadogAPIConfiguration.user_id == user.id)
        .all()
    )

    return JSONResponse(
        {
            "data": [
                {
                    "id": config.id,
                    "type": "datadog",
                }
                for config in configurations
            ]
        }
    )
