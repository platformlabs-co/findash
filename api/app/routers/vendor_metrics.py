import logging

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from app.helpers.auth import get_authenticated_user

logger = logging.getLogger(__name__)


router = APIRouter(tags=["cloud-cost-data"])


@router.get("/v1/vendors-metrics")
async def home(request: Request, auth_user: dict = Depends(get_authenticated_user)):
    return JSONResponse(
        {"data": {"message": "Welcome to the FinDash API", "user": auth_user}}
    )
