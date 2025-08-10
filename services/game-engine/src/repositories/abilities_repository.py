from typing import List, Optional
from sqlalchemy.orm import joinedload, selectinload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from models.user_character_ability import UserCharacterAbility
from models.ability_prerequisite import AbilityPrerequisite
from models.ability import Ability
from utils.constants import Constants
from utils.serializers import Serializer
import logging

logger = logging.getLogger(__name__)

class AbilitiesRepository:
    """
    Service class for abilities-related operations, including assignment and skill tree tracking
    """
    
    serializer = Serializer()

    
    """Util Methods"""
    
    
    
    """Getter Methods"""
    
    async def get_available_abilities(self):
        """Get abilities a user character is currently able to get based off of prereqs"""
        pass
    
    async def get_abilities_for_user_character(self, user_char_id: int):
        """Get abilities for a character claimed by a user"""
        with database_manager.get_db_session() as session:
            # user = session.query(User).filter_by(discord_id=user_id).first()
            # if not user:
            #     return Constants.USER_NOT_FOUND, None
            
            abilities = session.query(UserCharacterAbility)\
                .options(joinedload(UserCharacterAbility.ability),
                         joinedload(UserCharacterAbility.user_character))\
                .filter(UserCharacterAbility.user_character_id == user_char_id)\
                .all();
                
            logger.info(abilities)
            
            return Constants.SUCCESS, [self.serializer.serialize_user_character_ability(ability) for ability in abilities]
    
    """Setter Methods"""

    async def set_ability_to_user_character(self, user_char_id:int, ability_id:int) -> tuple[Constants, Optional[dict]]:
        """Set ability for a character claimed by a user"""
        with database_manager.get_db_session() as session:

            userAbility = UserCharacterAbility(
                user_character_id=user_char_id,
                ability_id=ability_id
            )
            session.add(userAbility)
            session.commit()
            session.refresh(userAbility)
            return Constants.SUCCESS, self.serializer.serialize_user_character_ability(userAbility)
        
        return Constants.ERROR, None
        