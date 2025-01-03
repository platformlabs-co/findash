import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Creating users table")

    try:
        with engine.begin() as conn:
            logger.info("Creating users table...")
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    sub VARCHAR UNIQUE NOT NULL,
                    email VARCHAR UNIQUE,
                    name VARCHAR,
                    picture VARCHAR,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """
                )
            )

            # Create indexes
            conn.execute(
                text(
                    """
                CREATE INDEX IF NOT EXISTS idx_users_sub ON users(sub);
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
            """
                )
            )

            logger.info("Users table created successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    upgrade()
