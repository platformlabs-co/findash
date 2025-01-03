import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.services.aws_service import AWSService
from app.services.datadog_service import DatadogService
from app.models import DatadogAPIConfiguration, AWSAPIConfiguration

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/vendors-metrics", tags=["vendors"])


def get_user(
    auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{vendor}")
async def get_vendor_metrics(
    vendor: str, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    if vendor.lower() == "datadog":
        config = (
            db.query(DatadogAPIConfiguration)
            .filter(DatadogAPIConfiguration.user_id == user.id)
            .first()
        )
    elif vendor.lower() == "aws":
        config = (
            db.query(AWSAPIConfiguration)
            .filter(AWSAPIConfiguration.user_id == user.id)
            .first()
        )
    else:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Unsupported vendor: {vendor}",
                "code": "INVALID_VENDOR",
            },
        )
    if not config:
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"No configuration found for vendor: {vendor}",
                "code": "CONFIG_NOT_FOUND",
            },
        )

    if vendor.lower() == "datadog":
        service = DatadogService(user.id, db)
        return service.get_monthly_costs()
    elif vendor.lower() == "aws":
        service = AWSService(user.id, db)
        return service.get_monthly_costs()
    else:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Unsupported vendor: {vendor}",
                "code": "INVALID_VENDOR",
            },
        )
