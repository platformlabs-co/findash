
from fastapi.security import HTTPBearer
import jwt
import os
from fastapi import Request, Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
import logging
from app.models import User
from app.helpers.database import get_db
from app.helpers.config import Config

logger = logging.getLogger(__name__)

ALGORITHMS = ["RS256"]

token_auth_scheme = HTTPBearer()


def validate_jwt(jwt_access_token):
    config = Config()
    
    auth0_issuer_url: str = f"https://{config.Auth0Domain}/"
    auth0_audience: str = config.Auth0Audience
    jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"
    
    logger.info(f"Getting JWT from the server {jwks_uri}")
    jwks_client = jwt.PyJWKClient(jwks_uri)
    jwt_signing_key = jwks_client.get_signing_key_from_jwt(
        jwt_access_token
    ).key
    payload = jwt.decode(
        jwt_access_token,
        jwt_signing_key,
        algorithms=ALGORITHMS,
        audience=auth0_audience,
        issuer=auth0_issuer_url,
    )
    return payload


async def get_authenticated_user(
    request: Request, 
    token: HTTPBearer = Depends(token_auth_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = validate_jwt(token.credentials)
        sub = payload["sub"]
        
        # Check if user exists, create if not
        db_user = db.query(User).filter(User.sub == sub).first()
        if not db_user:
            db_user = User(sub=sub)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        user = {
            "sub": sub,
            "token": token.credentials,
        }
        request.session["user"] = user
        return user
    except InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
