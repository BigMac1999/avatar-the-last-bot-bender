from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from fastapi import HTTPException, Response, status
from database.connection import database_manager
from database.migrations import MigrationRunner
from repositories.character_repository import CharacterRepository
from repositories.user_repository import UserRepository
from services.game_service import GameService
from services.character_service import CharacterService
from services.battle_service import BattleService
from services.abilities_service import AbilitiesService
from utils.response import APIResponse
from utils.constants import Constants

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

game_service = GameService()
char_service = CharacterService()
battle_service = BattleService()
ability_service = AbilitiesService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    """Initialize database connection and run migrations on startup."""
    await database_manager.connect()
    logger.info("Game Engine started and database connected")
    
    # Create tables from SQLAlchemy models
    database_manager.create_tables()
    logger.info("SQLAlchemy tables created/updated")
    
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
    health_dict = {"status": "ok", "message": "Game Engine is running"}
    return APIResponse.success(health_dict)

@app.get("/health")
async def health_check():
    """Health check with database connection status"""
    health_status = await database_manager.health_check()
    health_dict =  {
        "status": health_status.get("status", "unknown"),
        "message": health_status.get("message", "No message provided"),
        "test_query": health_status.get("test_query", "not executed")
    }
    return APIResponse.success(health_dict)
    
@app.get("/migrations")
async def migration_status():
    """Get migration status"""
    migration_runner = MigrationRunner(database_manager)
    status = await migration_runner.get_migration_status()
    return APIResponse.success(status)

"""User-related endpoints"""
@app.get("/users")
async def get_all_users():
    """Fetch all users from the database"""
    try:
        get_all_users_result = await game_service.get_all_users()
        
        if get_all_users_result != []:
            return APIResponse.success(get_all_users_result)
        return APIResponse.not_found("No users found")
    except Exception:
        return APIResponse.error("Failed to get all users")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Fetch a user by ID"""
    try:
        get_user_result = await game_service.get_user_by_id(user_id)
        if get_user_result is not None: 
            return APIResponse.success(get_user_result)
        return APIResponse.not_found("User not found")
    except Exception:
        return APIResponse.error(f"Failed to fetch user {user_id}")

@app.post("/users/{user_id}")
async def add_user(
    user_id: int, 
    username: str):
    """Add a user"""
    try:
        result_type, add_user_result = await game_service.onboard_user(user_id, username)
        if result_type == Constants.CREATED:
            return APIResponse.success(add_user_result)
        elif result_type == Constants.ALREADY_EXISTS:
            return APIResponse.conflict("User already exists")
    except Exception:
        return APIResponse.error(f"Failed to add user {user_id} {username}")

"""Character-related endpoints"""

@app.get("/characters")
async def get_all_characters():
    """Fetch all characters from the database"""
    result = await char_service.get_all_characters()
    return APIResponse.success(result)

@app.get("/characters/name/{character_name}")
async def get_character_by_name(character_name: str):
    """Fetch a character by name"""
    result = await char_service.get_char_by_name(character_name)
    if result:
        return APIResponse.success(result)
    return APIResponse.error("Character not found")

@app.get("/characters/id/{character_id}")
async def get_character_by_id(character_id: int):
    """Fetch a character by id"""
    result = await char_service.get_char_by_id(character_id)
    if result: 
        return APIResponse.success(result)
    return APIResponse.error("Character not found")

"""Abilities related endpoints"""
@app.get("/abilities/{ability_id}")
async def get_ability_by_id(ability_id: int):
    """Fetch details for an ability by its ID"""
    try:
        result_type, result_data = await ability_service.get_ability_by_id(ability_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.NOT_FOUND:
            return APIResponse.not_found(f"Ability id {ability_id} was not found.")
    except Exception as e:
        return APIResponse.error(f"Failed to find details for ability id {ability_id}: {e}")
    
@app.get("/abilities/nest/prereq/{ability_id}")
async def get_prereq_info(ability_id: int):
    """Fetch info on the prereqs for an ability"""
    try:
        result_type, result_data = await ability_service.get_nested_prereqs_for_an_ability(ability_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
    except Exception as e:
        return APIResponse.error(f"Failed to find prereqs for ability id {ability_id}: {e}")

"""User-Character Related endpoints"""

@app.get("/users/{user_id}/characters")
async def get_user_characters(user_id: int):
    """Fetch all characters ID claimed by a single user"""
    try:
        result_type, result_data = await char_service.get_all_user_characters(user_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.NOT_FOUND:
            return APIResponse.not_found(f"Characters for the user {user_id} were not found.")
        elif result_type == Constants.USER_NOT_FOUND:
            return APIResponse.not_found(f"User {user_id} was not found.")
    except Exception as e:
        return APIResponse.error(f"Failed to find characters for user {user_id}: {e}")
    
@app.post("/users/{user_id}/characters")
async def set_user_character(user_id: int, character_id: int):
    """Set a character for a user""" 
    try:
        result_type, result_data = await char_service.set_new_user_character(user_id=user_id, character_id=character_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.ALREADY_EXISTS:
            return APIResponse.not_found(f"Character {character_id} for the user {user_id} already existed.")
        elif result_type == Constants.USER_NOT_FOUND:
            return APIResponse.not_found(f"User {user_id} was not found to add character {character_id} to.")
    except Exception as e:
        return APIResponse.error(f"Failed to set character id {character_id} for user {user_id}: {e}")
    
@app.delete("/users/{user_id}/characters")
async def unset_user_character(user_id: int, character_id: int):
    """Remove a character for a user"""
    try:
        result_type, result_data = await char_service.unset_user_character(user_id=user_id, character_id=character_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.USER_NOT_FOUND:
            return APIResponse.not_found(f"User {user_id} was not found to add character {character_id} to.")
        elif result_type == Constants.NOT_FOUND:
            return APIResponse.not_found(f"Character id {character_id} was not found under user id {user_id} to delete.")
    except Exception as e:
        return APIResponse.error(f"Failed to delete character id {character_id} for user {user_id}: {e}")

@app.get("/users/{user_id}/roster")
async def get_user_roster(user_id: int):
    """Fetch all details for characters claimed by a single user"""
    try:
        result_type, result_data = await char_service.get_users_roster(user_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.NOT_FOUND:
            return APIResponse.not_found(f"Characters for the user {user_id} were not found.")
        elif result_type == Constants.USER_NOT_FOUND:
            return APIResponse.not_found(f"User {user_id} was not found.")
    except Exception as e:
        return APIResponse.error(f"Failed to find characters for user {user_id}: {e}")
    
"""Battle Related Endpoints"""



"""Manual Test Endpoints"""

@app.get("/characters/test/{user_id}/{character_id}/xp/{xp}")
async def test_add_xp_to_user(user_id:int, character_id: int, xp: int):
    """Test method to add XP to a user's character"""
    try:
        result_type, result_data = await battle_service.increase_exp(user_id, character_id, xp)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.NOT_FOUND:
            return APIResponse.not_found(f"Unable to find character {character_id} for user {user_id}")
        elif result_type == Constants.USER_NOT_FOUND:
            return APIResponse.not_found(f"User {user_id} was not found.")
    except Exception as e:
        return APIResponse.error(f"Failed to add xp {xp} for character {character_id} for user {user_id}: {e}")
    
@app.post("/character/test/ability/{user_char_id}/{ability_id}")
async def add_ability_to_user_char(user_char_id:int, ability_id:int):
    """Test method to add ability to a user's character"""
    try:
        result_type, result_data = await ability_service.set_ability_to_user_character(user_char_id, ability_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.FAILED and result_data:
            return APIResponse.error(f"Prerequisite abilities {result_data['missing_prerequisites']} not met for ability {ability_id} for character {user_char_id}")
        elif result_type == Constants.ALREADY_EXISTS:
            return APIResponse.already_exists(f"User character {user_char_id} already has ability {ability_id}")
    except Exception as e:
        return APIResponse.error(f"Failed to add ability {ability_id} for character {user_char_id}: {e}")
    
@app.get("/character/test/ability/{user_char_id}")
async def get_abilities_for_user_char(user_char_id:int):
    try:
        result_type, result_data = await ability_service.get_abilities_for_user_character(user_char_id)
        if result_type == Constants.SUCCESS:
            return APIResponse.success(result_data)
        elif result_type == Constants.NO_CONTENT:
            return APIResponse.no_content("No content found for this method")
    except Exception as e:
        return APIResponse.error(f"Failed to get abilities for character {user_char_id}: {e}")
        



# @app.get("/battle/test/xp/{xp}/")
# async def battle(

# BigMacs Todos
# TODO: Implement the battle engine for the bot (Python)
# TODO: Implement a test file to run endpoints to validate the battle engine (bash using curls)
# DONE: Implement postman collection for local testing
# DONE: Implement the character collection mechanism (SQL + Python)
# DONE: Implement the roster command to return all characters (SQL + Python) 
# DONE: Implement the stats command to return basic character stats (SQL + Python)
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
# DONE: Implement the logic to onboard a new user to the bot (Python + SQL)
# TODO INPROG: Begin to seed the database with characters (Python + SQL)