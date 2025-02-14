import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Adding updated_at to vendor metrics")
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    ALTER TABLE vendor_metrics
                    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE
                    DEFAULT CURRENT_TIMESTAMP;
                    """
                )
            )
            logger.info("Added updated_at column successfully")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


def downgrade():
    logger.info("Starting downgrade: Removing updated_at from vendor metrics")
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    ALTER TABLE vendor_metrics
                    DROP COLUMN IF EXISTS updated_at;
                    """
                )
            )
            logger.info("Removed updated_at column successfully")
    except Exception as e:
        logger.error(f"Downgrade failed: {str(e)}")
        raise


if __name__ == "__main__":
    upgrade()
