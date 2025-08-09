from repositories.character_repository import CharacterRepository
from repositories.battle_repository import BattleRepository
from services.character_service import CharacterService
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from utils.constants import Constants
from typing import Any, Optional, List

import logging

logger = logging.getLogger(__name__)

class BattleService:
    """
    Service class for battle-related operations, including exp, battles, etc
    """
    battle_repo = BattleRepository()
    character_repository = CharacterRepository()
    character_service = CharacterService()
    
    """Util Methods"""
    def level_up_check(self, userCharacterData: dict) -> bool:
        """
        Check if the character will level up with the increase in EXP
        """
        if userCharacterData['experience'] >= (10 * (userCharacterData['level'] ** 1.5)):
            return True
        return False
    
    def level_up(self, userCharacterData: dict):
        """Actually level up the character and call for stats increases"""
            
        while userCharacterData['experience'] >= 10 * (userCharacterData['level'] ** 1.5):
            logger.info("needs to level up once")
            userCharacterData['experience'] -= round(10 * (userCharacterData['level'] ** 1.5),2)
            userCharacterData['level'] += 1
            self.level_up_stats_increase(userCharacterData)
        
    
    def level_up_stats_increase(self, userCharacterData: dict):
        """Increase the stats of a character. This is its own method for future updates"""
        userCharacterData['current_hp'] *= round(1.10 ** (userCharacterData['level'] - 1),2)
        userCharacterData['current_attack'] *= round(1.08 ** (userCharacterData['level'] - 1),2)
        
    
    """Getter Methods"""
    
    
    
    """Setter Methods"""

    async def increase_exp(self, user_id: int, character_id: int, exp: int) -> tuple[Constants, Optional[dict]]:
        """Increase the EXP of a character and level up if needed."""
        status, userCharacterData = await self.character_service.get_single_user_character(user_id, character_id)
        
        if status != Constants.SUCCESS or userCharacterData is None:
            return status, None
        
        userCharacterData['experience'] += exp
                
        if self.level_up_check(userCharacterData):
            self.level_up(userCharacterData)
            
        statusCode, data = await self.character_repository.update_users_character(
            user_id,
            character_id,
            level=userCharacterData['level'],
            experience=userCharacterData['experience'],
            current_hp=userCharacterData['current_hp'],
            current_attack=userCharacterData['current_attack']
        )
            
        return statusCode, data
        
        
        