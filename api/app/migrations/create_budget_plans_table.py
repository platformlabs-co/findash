import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    logger.info("Starting migration: Creating budget_plans table")

    try:
        with engine.begin() as conn:
            logger.info("Creating budget_plans table...")
            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS budget_plans (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    vendor VARCHAR NOT NULL,
                    type VARCHAR NOT NULL DEFAULT 'default',
                    budgets JSONB NOT NULL,
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
                CREATE INDEX IF NOT EXISTS idx_budget_plans_user_id
                ON budget_plans(user_id)
            """
                )
            )

            conn.execute(
                text(
                    """
                CREATE INDEX IF NOT EXISTS idx_budget_plans_vendor
                ON budget_plans(vendor)
            """
                )
            )

            logger.info("Budget plans table created successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise
