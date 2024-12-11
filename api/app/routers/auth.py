from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.helpers.auth import OAuth

router = APIRouter(
    tags=["auth"]
)

@router.get('/v1/vendor-metrics')
async def home(request: Request):
    user = request.session.get('user')
    if user:
        return JSONResponse({"data": {
            "oauth_user": user
        }})
    return JSONResponse({"error_message": "You are not logged in."}, status_code=401)


@router.get('/')
async def home(request: Request):
    user = request.session.get('user')
    if user:
        return JSONResponse({"data": {
            "oauth_user": user
        }})
    return JSONResponse({"error_message": "You are not logged in."}, status_code=401)

@router.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?client_id={env.get('AUTH0_CLIENT_ID')}&returnTo={request.url_for('home')}")
