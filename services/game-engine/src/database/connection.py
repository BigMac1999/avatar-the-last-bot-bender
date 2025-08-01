import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

logger = logging.getLogger(__name__)

# Base class for all SQLAlchemy models
Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://atla_user:password@localhost:5432/atla_db")
        # Create engine with connection pooling
        self.engine = create_engine(
            self.database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Validates connections before use
            echo=False  # Set to True to see SQL queries in logs
        )
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    async def connect(self):
        """Initialize database connection and test it."""
        try:
            # Test the connection
            await self.health_check()
            logger.info("SQLAlchemy database connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """Dispose of the engine connection pool."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")

    async def health_check(self):
        """Check if the database connection is healthy."""
        try:
            with self.get_db_session() as session:
                # Test query using SQLAlchemy
                result = session.execute(text("SELECT 1"))
                result.fetchone()
            
            logger.info("Database connection is healthy")
            return {"status": "connected", "test_query": "SELECT 1", "message": "Database connection is healthy"}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "error", "message": str(e)}

    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """Context manager to get a database session."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()  # Commit the transaction if no exceptions
        except Exception as e:
            session.rollback()  # Rollback on exception
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()  # Always close the session

    def create_tables(self):
        """Create all tables defined in models."""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created/updated")

# Global database manager instance
database_manager = DatabaseManager()