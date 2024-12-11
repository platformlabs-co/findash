from os import environ as env
import logging

logging.basicConfig(level=logging.DEBUG)

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import find_dotenv, load_dotenv

from app.routers import auth
from app.helpers.auth import OAuth


def setup_app():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)


    app = FastAPI()
    OAuth().register()
    app.add_middleware(SessionMiddleware, secret_key=env.get('SECRET_KEY'))

    return app


app = setup_app()

app.include_router(auth.router)
