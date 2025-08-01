import os
import logging
import asyncio
from typing import List, Set
from pathlib import Path

logger = logging.getLogger(__name__)

class MigrationRunner:
    def __init__(self, database_manager):
        self.db_manager = database_manager
        self.migrations_dir = Path(__file__).parent / "migrations"

    async def initialize_migration_table(self):
        """Create the schema_migrations table if it doesn't exist."""
        try:
            # Updated to use SQLAlchemy session instead of raw psycopg2
            with self.db_manager.get_db_session() as session:
                from sqlalchemy import text
                session.execute(text("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version VARCHAR(255) PRIMARY KEY,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                logger.info("Migration table tracking ensured (SQLAlchemy)")
                
        except Exception as e:
            logger.error(f"Failed to create migration table: {e}")
            raise
        
    async def get_applied_migrations(self) -> Set[str]:
        """Get a set of applied migration versions."""
        try:
            # Updated to use SQLAlchemy session
            with self.db_manager.get_db_session() as session:
                from sqlalchemy import text
                result = session.execute(text("SELECT version FROM schema_migrations ORDER BY version"))
                applied = {row[0] for row in result.fetchall()}
                return applied
        except Exception as e:
            logger.error(f"Failed to fetch applied migrations: {e}")
            raise
        
    def get_migration_files(self) -> List[str]:
        """Get sorted list of migration files"""
        if not self.migrations_dir.exists():
            logger.warning(f"Migrations directory not found: {self.migrations_dir}")
            return []
        
        migration_files = []
        for file_path in sorted(self.migrations_dir.glob("*.sql")):
            migration_files.append(file_path.stem)  # filename without extension
        
        return migration_files
    
    async def apply_migration(self, migration_name: str):
        """Apply a single migration."""
        migration_file = self.migrations_dir / f"{migration_name}.sql"
        
        if not migration_file.exists():
            raise FileNotFoundError(f"Migration file not found: {migration_file}")
        
        logger.info(f"Applying migration: {migration_name}")
        
        try:
            # Read migration SQL
            with open(migration_file, 'r') as file:
                migration_sql = file.read()
                
            # Apply migration using SQLAlchemy session
            with self.db_manager.get_db_session() as session:
                from sqlalchemy import text
                
                # Execute the SQL commands
                session.execute(text(migration_sql))
                
                # Record that the migration was applied
                session.execute(
                    text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                    {"version": migration_name}
                )
                # Session automatically commits on context exit
                
            logger.info(f"Migration {migration_name} applied successfully (SQLAlchemy)")
            
        except Exception as e:
            logger.error(f"Failed to apply migration {migration_name}: {e}")
            raise
        
    async def run_migrations(self):
        """Run all pending migrations."""
        logger.info("Starting migration process...")
        
        #Ensure migration tracking table exists
        await self.initialize_migration_table()
        
        # Get current state
        applied_migrations = await self.get_applied_migrations()
        available_migrations = self.get_migration_files()
        
        #Find pending migrations
        pending_migrations = [
            migration for migration in available_migrations
            if migration not in applied_migrations
        ]
        
        if not pending_migrations:
            logger.info("No pending migrations found.")
            return
        
        logger.info(f"Found {len(pending_migrations)} pending migrations: {pending_migrations}")
        
        # Apply each pending migration
        for migration in pending_migrations:
            try:
                await self.apply_migration(migration)
            except Exception as e:
                logger.error(f"Migration {migration} failed: {e}")
                raise

        logger.info("All pending migrations applied successfully.")
        
    async def get_migration_status(self):
        """Get status of all migrations for debugging"""
        applied_migrations = await self.get_applied_migrations()
        available_migrations = self.get_migration_files()
        
        status = {
                "applied": list(applied_migrations),
                "available": available_migrations,
                "pending": [m for m in available_migrations if m not in applied_migrations]
            }
            
        return status