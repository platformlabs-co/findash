from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv
from app.helpers.secrets_service import SecretsService
import os


@dataclass
class Config:
    AppSecretKey: str
    Auth0Domain: str
    Auth0Audience: str

    def __init__(self):
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)
            
        secrets = SecretsService()
        self.AppSecretKey = secrets.get_secret("APP_SECRET_KEY", os.getenv("APP_SECRET_KEY"))
        self.Auth0Domain = secrets.get_secret("AUTH0_DOMAIN", os.getenv("AUTH0_DOMAIN"))
        self.Auth0Audience = secrets.get_secret("API_AUDIENCE", os.getenv("API_AUDIENCE", ""))
