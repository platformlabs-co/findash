from fastapi import APIRouter, Depends, HTTPException
from ..services.datadog_service import DatadogService
from ..services.aws_service import AWSService
from ..auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/v1/vendors-metrics", tags=["vendors"])


@router.get("/{vendor}", dependencies=[Depends(JWTBearer())])
async def get_vendor_metrics(vendor: str):
    try:
        if vendor.lower() == "datadog":
            service = DatadogService()
        elif vendor.lower() == "aws":
            service = AWSService()
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported vendor: {vendor}")

        return await service.get_monthly_costs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
