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
    
    
    """Battle Specific Methods"""
        
    async def create_battle_request_user(self, user_id: int, opponent_id: int) -> tuple[Constants, Optional[dict]]:
        """Create a new battle request for user v user"""
        try:
            return await self.battle_repo.create_battle_request_user(user_id, opponent_id, battle_type="user")
        except Exception as e:
            logger.error(f"Failed to create user battle request between user {user_id} and user {opponent_id}: {e}")
            raise
        
    async def create_battle_bot(self, user_id: int, opponent_id: int):
        """Create battle for user v bot"""
        try:
            # Create Postgres entry for the battle
            result_type, result_data =  await self.battle_repo.create_battle_bot(user_id, opponent_id, battle_type="bot")
        
            if result_type == Constants.SUCCESS and result_data is not None:
                await self.create_redis_battle()
                return Constants.SUCCESS, result_data
            
            return Constants.ERROR, None
        except Exception as e:
            logger.error(f"Failed to create battle request between user {user_id} and enemy {opponent_id}: {e}")
            raise
        
    async def update_battle_request_user(self, user_id: int, battle_id: int, response: str) -> tuple[Constants, Optional[dict]]:
        """Update a battle request for user v user"""
        try:
            battle_status, battle = await self.battle_repo.get_battle(battle_id)
            
            if battle_status != Constants.SUCCESS:
                return Constants.NOT_FOUND, None
            
            if battle == None:
                return Constants.INTERNAL_SERVER_ERROR, None
            
            if (battle['id'] == battle_id) and (battle['opponent_id'] == user_id):
                if battle['status'] == "in_progress" or battle['status'] == "completed":
                    return Constants.ALREADY_EXISTS, None
                
                if response == "yes":
                    result_type, result_data =  await self.battle_repo.update_battle(battle_id, status="in_progress")
                
                    if result_type == Constants.SUCCESS and result_data is not None:
                        await self.create_redis_battle() 
                        return Constants.SUCCESS, result_data
                elif response == "no":
                    return await self.battle_repo.update_battle(battle_id, status="cancelled")
            elif (battle['id' == battle_id]) and (battle['opponent_id'] != user_id):
                return Constants.CONFLICT, None
            
            return Constants.BAD_REQUEST, None
        
        except Exception as e:
            logger.error(f"Failed to update battle request for user {user_id} for battle {battle_id}: {e}")
            raise
    
    async def update_battle(self, battle_id: int, **updates):
        """Update an existing battle ()"""
        try:
            return await self.battle_repo.update_battle(battle_id, **updates)
        except Exception as e:
            logger.error(f"Failed to update battle id {battle_id}: {e}")
            raise
        
    async def create_redis_battle(self):
        # Need to format dicts that will be implemented into the redis cache
        
        # Get user 1 character list with abilities
        
        # Get user 2 character list with abilities
        
        
        
        pass
    
    async def return_redis_battle_state_dict(self):
#  TODO:  9. Implement team snapshot creation at battle start to freeze team composition and abilities

#   10. Create Redis methods to store immutable team snapshots (character stats, abilities, levels)

#   11. Separate current battle state (HP/MP/effects) from immutable snapshot data

#   12. Update battle initialization to capture both teams' complete state at battle creation

        return {
            "battle_id": "",
            "status": "",
            "battle_type": "",
            "created_at": "",
            "last_modified": "",
            "participants": {
                "user1": "",
                "user2": ""
            },
            "turn_data": {
                "current_turn": "",
                "current_player": "",
                "turn_order": [],
                "turn_started_at": "",
            },
            "battle_rules": {
                "max_team_size": "",
                "max_turns": "",
                "swap_cooldown": "",
                "battle_stats": {
                    "total_damage_dealt": "",
                    "character_swaps": "",
                    "turns_elapsed": ""
                }
            }
        }
        
