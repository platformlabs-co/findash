from fastapi import FastAPI
from app.helpers.database import init_db
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vendor_metrics, users, forecast
from app.helpers.config import Config
from app.helpers.database import Base, engine
import logging

logging.basicConfig(level=logging.DEBUG)

# Create database tables
Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)


def setup_app():
    app = FastAPI()
    init_db()

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
app.include_router(users.router, prefix="")
app.include_router(forecast.router)
