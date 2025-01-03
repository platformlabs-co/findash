from pydantic import BaseModel


class DatadogAPIConfig(BaseModel):
    app_key: str | None = None
    api_key: str | None = None


class AWSAPIConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str


class APIConfigResponse(BaseModel):
    id: int
    type: str
    message: str


class UserProfile(BaseModel):
    email: str | None = None
    name: str | None = None
    picture: str | None = None
