from repositories.enemy_repository import EnemyRepository
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from utils.constants import Constants
from typing import Any, Optional, List

import logging

logger = logging.getLogger(__name__)

class EnemyService:
    """
    Service class for enemy-related operations, including retrieval
    """
    enemy_repo = EnemyRepository()
    
    
    """Getter Methods"""
    
    async def get_all_enemies(self):
        """Get all enemies"""
        try:
            return await self.enemy_repo.get_all_enemies()
        except Exception as e:
            logger.error(f"Failed to retrieve all enemies: {e}")
            raise
        
    async def get_enemies_roster(self):
        """Get all enemies and their abilities"""
        try:
            return await self.enemy_repo.get_enemies_roster()
        except Exception as e:
            logger.error(f"Failed to retrieve enemies roster: {e}")
            raise
        
    async def get_single_enemy(self, enemy_id:int):
        """Get details for a single enemy"""
        try:
            return await self.enemy_repo.get_single_enemy_details(enemy_id)
        except Exception as e:
            logger.error(f"Failed to retrieve details for enemy {enemy_id}: {e}")
            raise