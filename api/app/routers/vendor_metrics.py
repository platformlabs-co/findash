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
from app.services.vendor_metrics_service import VendorMetricsService

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
    vendor: str,
    identifier: str = "Default Configuration",
    start_date: str = None,
    end_date: str = None,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    try:
        service = VendorMetricsService(user.id, db)
        return await service.get_and_store_vendor_metrics(vendor, identifier)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": str(e),
                "code": "INVALID_VENDOR",
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": str(e), "code": "VENDOR_ERROR"},
        )
