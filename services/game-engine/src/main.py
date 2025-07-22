from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection import database_manager

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database_manager.connect()
    logger.info("Game Engine started and database connected")
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