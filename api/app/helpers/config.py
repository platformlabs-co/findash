
from dataclasses import dataclass
import os

@dataclass 
class Config:
    AppSecretKey: str
    Auth0Domain: str
    Auth0Audience: str

    def __init__(self):
        self.AppSecretKey = os.environ.get("APP_SECRET_KEY")
        self.Auth0Domain = os.environ.get("AUTH0_DOMAIN") 
        self.Auth0Audience = os.environ.get("API_AUDIENCE", "")
