from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.services.aws_service import AWSService
from app.services.datadog_service import DatadogService

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
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    try:
        if vendor.lower() == "datadog":
            service = DatadogService(user.id, db, identifier=identifier)
            return await service.get_monthly_costs()
        elif vendor.lower() == "aws":
            service = AWSService(user.id, db, identifier=identifier)
            return await service.get_monthly_costs()
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"Unsupported vendor: {vendor}",
                    "code": "INVALID_VENDOR",
                },
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": str(e), "code": "VENDOR_ERROR"},
        )
