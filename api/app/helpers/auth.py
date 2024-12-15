from fastapi.security import HTTPBearer
import jwt
import os
from fastapi import Request, Depends, HTTPException
import jwt
from jwt.exceptions import InvalidTokenError
import os
import logging

logger = logging.getLogger(__name__)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE", "")
ALGORITHMS = ["RS256"]

token_auth_scheme = HTTPBearer()


class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    jwt_access_token: str
    auth0_issuer_url: str = f"https://{AUTH0_DOMAIN}/"
    auth0_audience: str = API_AUDIENCE
    algorithm: str = "RS256"
    jwks_uri: str = f"{auth0_issuer_url}.well-known/jwks.json"

    def validate(self):
        jwks_client = jwt.PyJWKClient(self.jwks_uri)
        jwt_signing_key = jwks_client.get_signing_key_from_jwt(
            self.jwt_access_token
        ).key
        payload = jwt.decode(
            self.jwt_access_token,
            jwt_signing_key,
            algorithms=self.algorithm,
            audience=self.auth0_audience,
            issuer=self.auth0_issuer_url,
        )
        return payload


async def get_authenticated_user(
    request: Request, token: HTTPBearer = Depends(token_auth_scheme)
):
    jwt_token = JsonWebToken()
    jwt_token.jwt_access_token = token.credentials
    try:
        payload = jwt_token.validate()
        user = {
            "sub": payload["sub"],
            "token": token.credentials,
        }
        request.session["user"] = user
        return user
    except InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
