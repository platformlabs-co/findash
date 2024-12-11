from authlib.integrations.starlette_client import OAuth as OAuthClient
from os import environ as env

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]\

class OAuth(metaclass=SingletonMeta):
    def __init__(self):
        self.oauth = None

    def register(self):
        self.oauth = OAuthClient()
        self.oauth.register(
            "auth0",
            client_id=env.get("AUTH0_CLIENT_ID"),
            client_secret=env.get("AUTH0_CLIENT_SECRET"),
            client_kwargs={
                "scope": "openid profile email",
            },
            server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
        )

    def get(self):
        return self.oauth