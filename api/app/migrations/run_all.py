import logging
import time
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def wait_for_db(max_retries=5, delay=5):
    """Wait for database to become available"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection successful")
                return True
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt + 1 < max_retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    return False


def run_migrations():
    """Run all migrations in order"""
    from app.migrations import MIGRATIONS

    if not wait_for_db():
        raise Exception("Could not connect to database after multiple retries")

    logger.info("Starting migrations...")

    for migration in MIGRATIONS:
        try:
            logger.info(f"Running migration: {migration.__name__}")
            migration()
        except Exception as e:
            logger.error(f"Migration {migration.__name__} failed: {e}")
            raise

    logger.info("All migrations completed successfully")


if __name__ == "__main__":
    run_migrations()
