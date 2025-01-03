import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Adding user profile fields")

    try:
        with engine.begin() as conn:
            logger.info("Executing ALTER TABLE statement...")
            conn.execute(
                text(
                    """
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS email VARCHAR,
                ADD COLUMN IF NOT EXISTS name VARCHAR,
                ADD COLUMN IF NOT EXISTS picture VARCHAR
            """
                )
            )
            logger.info("Migration completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    upgrade()
