import logging

logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vendor_metrics
from app.helpers.config import Config


logger = logging.getLogger(__name__)


def setup_app():

    app = FastAPI()

    config = Config()
    app.add_middleware(SessionMiddleware, secret_key=config.AppSecretKey)

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with your specific URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = setup_app()

app.include_router(vendor_metrics.router)
