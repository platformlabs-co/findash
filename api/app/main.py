from os import environ as env
import logging

logging.basicConfig(level=logging.DEBUG)

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import find_dotenv, load_dotenv
from app.routers import auth
from app.helpers.auth import OAuth

logger = logging.getLogger(__name__)


def setup_app():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)


    app = FastAPI()
    OAuth().register()
    app.add_middleware(SessionMiddleware, secret_key=env["SECRET_KEY"])

    frontend_url = env["REACT_APP_FRONTEND_URL"]

    logger.info(f"Setting up CORS middleware to allow {frontend_url}") 
    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url, '*'],  # Replace with your specific URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = setup_app()

app.include_router(auth.router)
