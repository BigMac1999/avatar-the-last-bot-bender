from repositories.user_repository import UserRepository
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from constants.user_constants import UserOnboardResult, UserConstants
from typing import Any, Optional

import logging

logger = logging.getLogger(__name__)

class GameService:
    """
    Service class for game-related operations, including user onboarding and retrieval.
    """
    user_repo = UserRepository()

    async def get_all_users(self):
        """Get all users"""
        try: 
            return await self.user_repo.get_all_users()
        except Exception as e:
            logger.error(f"Failed to retrieve all users: {e}")
            raise
    
    async def get_user_by_id(self, user_id: int):
        """Get User by ID"""
        try: 
            return await self.user_repo.get_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Failed to retrieve user {user_id}: {e}")
            raise
        

    async def onboard_user(self, user_id: int, username: str) -> tuple[UserOnboardResult, Optional[dict]]:
        """Onboard the user to the game"""
        try:
            return await self.user_repo.onboard_user(user_id, username)
        except Exception as e:
            logger.error(f"Failed to onboard user {user_id} {username}: {e}")
            raise

