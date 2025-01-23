import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Adding identifier field to API configurations")

    try:
        with engine.begin() as conn:
            # Add identifier column to datadog configurations
            logger.info("Adding identifier column to datadog_api_configurations...")
            conn.execute(
                text(
                    """
                    ALTER TABLE datadog_api_configurations
                    ADD COLUMN IF NOT EXISTS identifier VARCHAR DEFAULT 'Default Configuration';
                    """
                )
            )

            # Add identifier column to aws configurations
            logger.info("Adding identifier column to aws_api_configurations...")
            conn.execute(
                text(
                    """
                    ALTER TABLE aws_api_configurations
                    ADD COLUMN IF NOT EXISTS identifier VARCHAR DEFAULT 'Default Configuration';
                    """
                )
            )

            # Remove old unique constraints
            logger.info("Removing old unique constraints...")
            conn.execute(
                text(
                    """
                    ALTER TABLE datadog_api_configurations
                    DROP CONSTRAINT IF EXISTS uq_datadog_user;
                    """
                )
            )

            conn.execute(
                text(
                    """
                    ALTER TABLE aws_api_configurations
                    DROP CONSTRAINT IF EXISTS uq_aws_user;
                    """
                )
            )

            # Add new unique constraints for user_id + identifier combinations
            logger.info("Adding new unique constraints for user_id + identifier...")
            conn.execute(
                text(
                    """
                    ALTER TABLE datadog_api_configurations
                    ADD CONSTRAINT uq_datadog_user_identifier UNIQUE (user_id, identifier);
                    """
                )
            )

            conn.execute(
                text(
                    """
                    ALTER TABLE aws_api_configurations
                    ADD CONSTRAINT uq_aws_user_identifier UNIQUE (user_id, identifier);
                    """
                )
            )

            logger.info("Migration completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    upgrade()
