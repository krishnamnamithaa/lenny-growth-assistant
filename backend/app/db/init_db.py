import logging
from sqlalchemy import text
from app.db.session import engine
from app.models.base import Base
import app.models # Ensure all models are registered with Base

logger = logging.getLogger(__name__)

def init_db(db_engine=engine) -> bool:
    """Initialize database tables and create pgvector extension if supported."""
    try:
        # Enable pgvector if connecting to PostgreSQL
        if "postgresql" in str(db_engine.url):
            with db_engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.commit()
                logger.info("pgvector extension checked/initialized.")
        
        # Create all tables
        Base.metadata.create_all(bind=db_engine)
        logger.info("Database tables initialized successfully.")
        return True
    except Exception as e:
        logger.warning(f"Database initialization deferred/offline: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
