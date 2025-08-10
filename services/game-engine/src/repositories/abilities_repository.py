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

    """Getter Methods"""
    
    async def get_nested_ability_prereqs(self, ability_id: int) -> tuple[Constants, Optional[dict]]:
        """Get complete prerequisite tree for an ability"""
        with database_manager.get_db_session() as session:
            tree = await self._build_prerequisite_tree(session, ability_id)
            
            if not tree["prerequisites"]:
                return Constants.NO_CONTENT, {
                    "ability_id": ability_id,
                    "prerequisites": [],
                    "message": "This ability has no prerequisites"
                }
                
            return Constants.SUCCESS, tree
        return Constants.ERROR, None
    
    async def _build_prerequisite_tree(self, session, ability_id: int, visited: set = None, level: int = 0) -> dict: # type: ignore
        """Recursively build prerequisite tree"""
        if visited is None:
            visited = set()
            
        # Prevent infinite loops
        if ability_id in visited:
            return {"ability_id": ability_id, "prerequisites": [], "level": level, "circular_reference": True}
            
        visited.add(ability_id)
        
        # Get direct prerequisites for this ability
        prereqs = session.query(AbilityPrerequisite)\
            .options(joinedload(AbilityPrerequisite.ability),
                    joinedload(AbilityPrerequisite.prerequisite_ability))\
            .filter(AbilityPrerequisite.ability_id == ability_id)\
            .all()
        
        # Build tree structure
        prerequisite_tree = []
        
        for prereq in prereqs:
            # Get prerequisite ability details
            prereq_data = self.serializer.serialize_ability_prereq(prereq)
            prereq_data["level"] = level
            
            # Recursively get prerequisites of this prerequisite
            subtree = await self._build_prerequisite_tree(
                session, 
                prereq.prerequisite_ability_id, 
                visited.copy(),  # Pass copy to allow different branches
                level + 1
            )
            
            # Add nested prerequisites to this prerequisite
            prereq_data["nested_prerequisites"] = subtree["prerequisites"]
            prerequisite_tree.append(prereq_data)
        
        visited.remove(ability_id)  # Remove from visited when backtracking
        
        return {
            "ability_id": ability_id,
            "prerequisites": prerequisite_tree,
            "level": level
        }
    
    async def get_abilities_for_user_character(self, user_char_id: int):
        """Get abilities for a character claimed by a user"""
        with database_manager.get_db_session() as session:
            abilities = session.query(UserCharacterAbility)\
                .options(joinedload(UserCharacterAbility.ability),joinedload(UserCharacterAbility.user_character))\
                .filter(UserCharacterAbility.user_character_id == user_char_id)\
                .all()
                
            if not abilities:
                return Constants.NOT_FOUND, None
                            
            return Constants.SUCCESS, [self.serializer.serialize_user_character_ability(ability) for ability in abilities]
    
    async def get_ability_by_id(self, ability_id: int):
        """Get details about an ability by its id"""
        with database_manager.get_db_session() as session:
            ability = session.query(Ability)\
                .filter(Ability.id==ability_id)\
                .first()
                
            if not ability:
                return Constants.NOT_FOUND, None
                
            return Constants.SUCCESS, self.serializer.serialize_ability(ability)
        return Constants.ERROR, None

    
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
        