from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv
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
        self.AppSecretKey = os.getenv("APP_SECRET_KEY")
        self.Auth0Domain = os.getenv("AUTH0_DOMAIN")
        self.Auth0Audience = os.getenv("API_AUDIENCE", "")
