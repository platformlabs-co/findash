import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Creating api_configurations table")

    try:
        with engine.begin() as conn:
            logger.info("Creating api_configurations table...")
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS api_configurations (
                    id SERIAL PRIMARY KEY,
                    type VARCHAR NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """
                )
            )

            # Create indexes
            conn.execute(
                text(
                    """
                CREATE INDEX IF NOT EXISTS idx_api_configurations_user_id
                ON api_configurations(user_id)
            """
                )
            )

            logger.info("API configurations table created successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    upgrade()
