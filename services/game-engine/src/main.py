from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection import database_manager
from database.migrations import MigrationRunner
from repositories.character_repository import CharacterRepository

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

"""Health check endpoints and migrations"""
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


# TODO: Add error handling for endpoints
# Currently, if an endpoint call has an error, it still returns a 200 status code
# TODO: Update migrations and sql tables today to handle more robust logic
"""Character-related endpoints (currently only for validation)"""

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

"""Future user-related endpoints (currently commented out)"""


# BigMacs Todos
# TODO: Implement the battle engine for the bot (Python)
# TODO: Implement a test file to run endpoints to validate the battle engine (bash using curls)
# TODO: Implement the character collection mechanism (SQL + Python)
# TODO: Implement the roster command to return all characters (SQL + Python) 
# TODO: Implement the stats command to return character stats (SQL + Python)
# TODO: Implement 3rd party blob storage for character images (Python + MinIO or similar)
# TODO: Implement the following stats to be returned for each character:
# - User battles won
# - User battles lost
# - Number of times user has rolled a character
# - Return abilities/skill tree for each character
# - Return active abilities for each character
# - Return general stats for each character
# TODO: Implement Discord OAuth for user authentication for the website(Python + Discord API)

# Bianca's TODOs
# TODO: Implement the roll command to roll a character (Python + SQL)
# TODO: Implement the website command to link to the expected http://localhost:3001 endpoint for local dev for now (Python)

# Both/Either TODOs
# TODO: Implement the logic to onboard a new user to the bot (Python + SQL)
# TODO: Begin to seed the database with characters (Python + SQL)