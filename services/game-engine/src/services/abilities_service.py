from repositories.abilities_repository import AbilitiesRepository
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from utils.constants import Constants
from typing import Any, Optional, List

import logging

logger = logging.getLogger(__name__)

class AbilitiesService:
    """
    Service class for abilities-related operations, including retrival
    """
    abilities_repo = AbilitiesRepository()
    
    """Getter Methods"""
    
    async def get_abilities_for_user_character(self, user_char_id:int):
        """Get abilities for a character claimed by a user"""
        try:
            return await self.abilities_repo.get_abilities_for_user_character(user_char_id)
        except Exception as e:
            logger.error(f"Failed to retrieve abilities for character id {user_char_id}: {e}")
            raise
        
        
    """Setter Methods"""
    async def set_ability_to_user_character(self, user_char_id:int, ability_id:int):
        """Set an ability for a user claimed character"""
        try:
            return await self.abilities_repo.set_ability_to_user_character(user_char_id, ability_id)
        except Exception as e:
            logger.error(f"Failed to set ability {ability_id} for character id {user_char_id}: {e}")
            raise