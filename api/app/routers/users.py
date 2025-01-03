import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from pydantic import BaseModel

logger = logging.getLogger(__name__)


router = APIRouter(tags=["users"])


class UserProfile(BaseModel):
    email: str
    name: str | None = None
    picture: str | None = None


@router.get("/v1/profile", response_model=UserProfile)
async def get_user_profile(
    auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
) -> UserProfile:
    """Get the profile of the currently authenticated user"""
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserProfile(email=user.email, name=user.name, picture=user.picture)
