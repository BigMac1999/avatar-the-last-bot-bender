from repositories.character_repository import CharacterRepository
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from constants.character_constants import CharConstants
from typing import Any, Optional, List

import logging

logger = logging.getLogger(__name__)

class CharacterService:
    """
    Service class for character-related operations, including retrieval
    """
    character_repo = CharacterRepository()

    async def get_all_characters(self):
        """Get all characters"""
        try: 
            return await self.character_repo.get_all_characters()
        except Exception as e:
            logger.error(f"Failed to retrieve all characters: {e}: {e}")
            raise
        
    async def get_char_by_name(self, char_name: str):
        """Get character by name"""
        try: 
            return await self.character_repo.get_character_by_name(char_name)
        except Exception as e:
            logger.error(f"Failed to retrieve character {char_name}: {e}")
            raise
            
    async def get_char_by_id(self, char_id: int):
        """Get character by ID"""
        try:
            return await self.character_repo.get_character_by_id(char_id)
        except Exception as e:
            logger.error(f"Failed to retrieve character ID {char_id}: {e}")
            raise
            
    async def get_all_char_of_element(self, element: str):
        """Get all characters of a specific element"""
        try:
            return await self.character_repo.get_characters_by_element(element)
        except Exception as e:
            logger.error(f"Failed to retrieve all characters of element {element}: {e}")
            raise

    async def get_all_user_characters(self, user_id:int) -> tuple[CharConstants, Optional[List[dict]]]:
        """Get all characters claimed by one user"""
        try:
            return await self.character_repo.get_users_characters(user_id)
        except Exception as e:
            logger.error(f"Failed to retrieve all characters of user {user_id}: {e}")
            raise
            
    async def set_new_user_character(self, user_id: int, char_id: int):
        """ Set a character for a user"""
        try:
            return await self.character_repo.set_character_to_user(user_id, char_id)
        except Exception as e:
            logger.error(f"Failed to set character id {char_id} for user id {user_id} : {e}")
            raise
        
    async def unset_user_character(self, user_id: int, char_id: int):
        """Remove a character from a user"""
        try:
            return await self.character_repo.unset_character_to_user(user_id, char_id)
        except Exception as e:
            logger.error(f"Failed to remove character id {char_id} for user id {user_id} : {e}")
            raise
