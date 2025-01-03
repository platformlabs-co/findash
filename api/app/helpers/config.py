from dataclasses import dataclass
from dotenv import find_dotenv, load_dotenv
import os


@dataclass
class Config:
    InfisicalClientId: str
    InfisicalClientSecret: str
    InfisicalProjectId: str
    Environment: str

    def __init__(self):
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)
        self.load_config()

    def load_config(self):
        self.InfisicalClientId = os.getenv("INFISICAL_CLIENT_ID")
        self.InfisicalClientSecret = os.getenv("INFISICAL_CLIENT_SECRET")
        self.InfisicalProjectId = os.getenv("INFISICAL_PROJECT_ID")
        self.Environment = os.getenv("ENVIRONMENT", "dev")
