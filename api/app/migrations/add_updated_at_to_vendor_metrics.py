import logging
from sqlalchemy import text
from app.helpers.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upgrade():
    logger.info("Starting migration: Adding updated_at to vendor_metrics table")

    try:
        with engine.begin() as conn:
            # Add updated_at column
            conn.execute(
                text(
                    """
                    ALTER TABLE vendor_metrics 
                    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;
                    
                    -- Update existing rows to have updated_at equal to created_at
                    UPDATE vendor_metrics 
                    SET updated_at = created_at 
                    WHERE updated_at IS NULL;
                    """
                )
            )

            logger.info("Successfully added updated_at column to vendor_metrics table")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise 