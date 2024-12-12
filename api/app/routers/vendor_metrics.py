from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from fastapi.security import HTTPBearer 

router = APIRouter(
    tags=["cloud-cost-data"]
)

token_auth_scheme = HTTPBearer()

@router.get('/v1/vendors-metrics')
async def home(request: Request, token: str = Depends(token_auth_scheme)):
    print(token)
    user = request.session.get('user')
    if user:
        return JSONResponse({"data": {
            "oauth_user": user
        }})
    return JSONResponse({"error_message": "You are not logged in."}, status_code=401)
