from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection import database_manager
from database.migrations import MigrationRunner
from repositories.character_repository import CharacterRepository
# from repositories.user_repository import UserRepository

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    """Initialize database connection and run migrations on startup."""
    await database_manager.connect()
    logger.info("Game Engine started and database connected")
    
    #Run database Migrations
    migration_runner = MigrationRunner(database_manager)
    await migration_runner.run_migrations()
    logger.info("Database migrations completed successfully, game engine started successfully")
    yield
    # Shutdown
    await database_manager.disconnect()
    logger.info("Game Engine stopped and database disconnected")

app = FastAPI(
    title="ATLA Game Engine",
    description="Game engine for Avatar: The Last Airbender companion app (FAN MADE)",       
    version="1.0.0",
    lifespan=lifespan
    )

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "ok", "message": "Game Engine is running"}

@app.get("/health")
async def health_check():
    """Health check with database connection status"""
    health_status = await database_manager.health_check()
    return {
        "status": health_status.get("status", "unknown"),
        "message": health_status.get("message", "No message provided"),
        "test_query": health_status.get("test_query", "not executed")
    }
    
@app.get("/migrations")
async def migration_status():
    """Get migration status"""
    migration_runner = MigrationRunner(database_manager)
    status = await migration_runner.get_migration_status()
    return status

@app.get("/characters")
async def get_all_characters():
    """Fetch all characters from the database"""
    result = await CharacterRepository().get_all_characters()
    return result

@app.get("/characters/{character_name}")
async def get_character_by_name(character_name: str):
    """Fetch a character by name"""
    result = await CharacterRepository().get_character_by_id(character_name)
    if result:
        return result
    return {"error": "Character not found"}