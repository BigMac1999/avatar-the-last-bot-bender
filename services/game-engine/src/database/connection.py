import asyncio
import psycopg2
from psycopg2 import pool
from typing import Optional, Dict, Any
import os
import logging
from contextlib import contextmanager


logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection_pool: Optional[pool.SimpleConnectionPool] = None
        self.database_url = os.getenv("DATABASE_URL", "postgresql://atla_user:password@localhost:5432/atla_db")

    async def connect(self):
        """Initialize the connection pool."""
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1, 20, self.database_url
            )
            logger.info("Database connections created successfully")

            #Test the connection
            await self.health_check()

        except Exception as e:
            logger.error(f"Failed to connect to database {e}")
            raise

    async def disconnect(self):
        """Close the connection pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Database connections closed")

    async def health_check(self):
        """Check if the database connection is healthy."""
        if not self.connection_pool:
            return {"status": "error", "message": "Connection pool not initialized"}
        try:
            # conn = self.connection_pool.getconn()
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")
                cursor.fetchone()
                cursor.close()

            logger.info("Database connection is healthy")
            return {"status": "connected", "test_query": "SELECT 1;", "message": "Database connection is healthy, test query executed successfully"}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "error", "message": str(e)}
        
    def get_connection(self):
        """Get a connection from the pool."""
        with self.get_db_connection() as conn:
            return conn
    
    def return_connection(self, conn):
        """Return a connection to the pool."""
        if not self.connection_pool:
            return {"status": "error", "message": "Connection pool not initialized"}
        
        self.connection_pool.putconn(conn)

    @contextmanager
    def get_db_connection(self):
        """Context manager to get a database connection."""
        if not self.connection_pool:
            raise Exception("Database connection pool is not initialized")
        
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error getting database connection: {e}")
            raise
        finally:
            if conn:
                self.connection_pool.putconn(conn)

database_manager = DatabaseManager()