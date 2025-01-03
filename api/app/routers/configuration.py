import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, DatadogAPIConfiguration, AWSAPIConfiguration
from app.routers.models import DatadogAPIConfig, AWSAPIConfig, APIConfigResponse
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.services.configuration_service import ConfigurationService

router = APIRouter(prefix="/v1/configuration", tags=["configuration"])

logger = logging.getLogger(__name__)


def get_user(
    auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/datadog")
async def configure_datadog(
    config: DatadogAPIConfig,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
) -> APIConfigResponse:
    secrets_data = {
        "DATADOG_APP_KEY": config.app_key,
        "DATADOG_API_KEY": config.api_key,
    }

    try:
        config_service = ConfigurationService(db, user)
        config_id, message = config_service.configure_vendor("datadog", secrets_data)

        return APIConfigResponse(id=config_id, type="datadog", message=message)
    except Exception as e:
        logger.error(f"Failed to configure Datadog: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to configure Datadog: {str(e)}"
        )


@router.post("/aws")
async def configure_aws(
    config: AWSAPIConfig,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
) -> APIConfigResponse:
    secrets_data = {
        "AWS_ACCESS_KEY_ID": config.aws_access_key_id,
        "AWS_SECRET_ACCESS_KEY": config.aws_secret_access_key,
    }

    config_service = ConfigurationService(db, user)
    try:
        config_id, message = config_service.configure_vendor("aws", secrets_data)

        return APIConfigResponse(id=config_id, type="aws", message=message)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to configure AWS: {str(e)}"
        )


@router.get("/list")
async def list_api_configurations(
    user: User = Depends(get_user), db: Session = Depends(get_db)
):
    datadog_configs = (
        db.query(DatadogAPIConfiguration)
        .filter(DatadogAPIConfiguration.user_id == user.id)
        .all()
    )

    aws_configs = (
        db.query(AWSAPIConfiguration)
        .filter(AWSAPIConfiguration.user_id == user.id)
        .all()
    )

    return {
        "data": [
            {
                "id": config.id,
                "type": "aws" if isinstance(config, AWSAPIConfiguration) else "datadog",
            }
            for config in (datadog_configs + aws_configs)
        ]
    }
