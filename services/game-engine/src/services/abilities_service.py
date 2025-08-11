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
    
    """Util Methods"""
    
    def _flatten_prerequisite_tree(self, tree: dict) -> set[int]:
        """Extract all prerequisite ability IDs from nested tree into flat set"""
        def _extract_ids(node):
            ids = set()
            if "prerequisite_ability_id" in node:
                ids.add(node["prerequisite_ability_id"])
            
            # Recursively extract from nested prerequisites
            for nested in node.get("nested_prerequisites", []):
                ids.update(_extract_ids(nested))
            return ids
        
        all_ids = set()
        for prereq in tree.get("prerequisites", []):
            all_ids.update(_extract_ids(prereq))
        
        return all_ids
    
    async def _get_user_abilities_batch(self, user_char_id: int, ability_ids: set[int]) -> dict[int, bool]:
        """Get which abilities from the set the user actually has"""
        if not ability_ids:
            return {}
        
        # Get user's abilities from repository
        status, user_abilities = await self.abilities_repo.get_abilities_for_user_character(user_char_id)
        
        if status != Constants.SUCCESS or not user_abilities:
            return {ability_id: False for ability_id in ability_ids}
        
        # Extract ability IDs user has
        user_has = {ability["ability_id"] for ability in user_abilities}
        
        # Return mapping: ability_id -> has_ability
        return {ability_id: ability_id in user_has for ability_id in ability_ids}
    
    async def check_user_has_prerequisites(self, user_char_id: int, ability_id: int) -> tuple[Constants, Optional[dict]]:
        """Check if user has all prerequisites for an ability"""
        try:
            # Get the nested prerequisite tree
            char_status, char_data = await self.abilities_repo.check_if_character_can_learn_ability(ability_id, user_char_id)
            status, tree = await self.abilities_repo.get_nested_ability_prereqs(ability_id)
            # if status != Constants.SUCCESS or char_status != Constants.SUCCESS:
            #     return status, tree or {}
            
            if tree is None and char_data is None:
                return Constants.ERROR, {
                    "message": "Unable to retrieve prerequisite data",
                    "ability_id": ability_id
                }
            elif char_data is None:
                return char_status, {
                    "message": "Character data not found",
                    "ability_id": ability_id
                }
            elif tree is None and status != Constants.NO_CONTENT:
                return status, {
                    "message": "Prerequisite tree not found", 
                    "ability_id": ability_id
                }
            
            if tree is None:
                return Constants.ERROR, None
            
            if char_status != Constants.SUCCESS:
                return char_status, char_data
            
            if status != Constants.SUCCESS and status != Constants.NO_CONTENT:
                return status, tree
            
            if status == Constants.NO_CONTENT:
                return Constants.NO_CONTENT, {
                    "ability_id": ability_id,
                    "has_all_prerequisites": True,
                    "missing_prerequisites": [],
                    "message": "No prerequisites required"
                }
            
            # Extract all prerequisite IDs from tree
            all_prereq_ids = self._flatten_prerequisite_tree(tree)
            
            # Check which abilities user has
            user_abilities = await self._get_user_abilities_batch(user_char_id, all_prereq_ids)
            
            # Find missing prerequisites
            missing = [ability_id for ability_id, has_ability in user_abilities.items() if not has_ability]
            
            if len(missing) > 0:
                return Constants.FAILED, {
                    "ability_id": ability_id,
                    "has_all_prerequisites": len(missing) == 0,
                    "missing_prerequisites": missing,
                    "prerequisite_check": user_abilities
                }
            
            return Constants.SUCCESS, {
                "ability_id": ability_id,
                "has_all_prerequisites": len(missing) == 0,
                "missing_prerequisites": missing,
                "prerequisite_check": user_abilities
            }
            
        except Exception as e:
            logger.error(f"Failed to check prerequisites for ability {ability_id} and user character {user_char_id}: {e}")
            return Constants.ERROR, {
                "message": f"Failed to check prerequisites: {str(e)}",
                "ability_id": ability_id
            }
    
    # async def check_abilities_max(self):
    #     """Check if a user has the max number of abilities selected."""
    #     #Post-MVP, i want users to have to select 4 abilities to have as active
    #     pass
    
    async def check_abilities_prereqs(self):
        """Check if an ability that is to be added to a user has the correct prereqs"""
        pass
    
    """Getter Methods"""
    
    async def get_abilities_for_user_character(self, user_char_id:int):
        """Get abilities for a character claimed by a user"""
        try:
            return await self.abilities_repo.get_abilities_for_user_character(user_char_id)
        except Exception as e:
            logger.error(f"Failed to retrieve abilities for character id {user_char_id}: {e}")
            raise
        
    async def get_ability_by_id(self, ability_id: int):
        """Get details about an ability by its id"""
        try:
            return await self.abilities_repo.get_ability_by_id(ability_id)
        except Exception as e:
            logger.error(f"Failed to retrieve details for ability id {ability_id}: {e}")
            raise
        
    async def get_nested_prereqs_for_an_ability(self, ability_id: int):
        """Get prereqs for an ability"""
        try:
            return await self.abilities_repo.get_nested_ability_prereqs(ability_id)
        except Exception as e:
            logger.error(f"Failed to retrieve prereqs for ability id {ability_id}: {e}")
            raise
        
    """Setter Methods"""
    async def set_ability_to_user_character(self, user_char_id: int, ability_id: int):
        """Set an ability for a user claimed character"""
        try:
            # # Check if user already has this ability
            user_abilities_status, user_abilities = await self.abilities_repo.get_abilities_for_user_character(user_char_id)
            
            if user_abilities:
                for ability in user_abilities:
                    if ability['ability_id'] == ability_id:
                        return Constants.ALREADY_EXISTS, {
                            "message": "Ability already claimed",
                            "ability_id": ability_id
                        } 
            
            # Check if user has all prerequisites
            prereq_status, prereq_result = await self.check_user_has_prerequisites(user_char_id, ability_id)
            
            
            if prereq_status == Constants.FAILED:
                if prereq_result:
                    return Constants.FAILED, {
                        "message": "Prerequisites not met", 
                        "missing_prerequisites": prereq_result["missing_prerequisites"],
                        "ability_id": ability_id
                    }
                else:
                    return Constants.FAILED, {
                        "message": "Prerequisites check failed", 
                        "missing_prerequisites": [],
                        "ability_id": ability_id
                    }
            elif prereq_status == Constants.SUCCESS or prereq_status == Constants.NO_CONTENT:
                # Prerequisites met or no prerequisites required - proceed to add ability
                return await self.abilities_repo.set_ability_to_user_character(user_char_id, ability_id)
            elif prereq_status == Constants.BAD_REQUEST:
                return Constants.FAILED, {
                    "message": "Character cannot learn this ability",
                    "missing_prerequisites": ["Character cannot learn this ability"],
                    "ability_id": ability_id
                }
            else:
                # Handle other status codes (ERROR, etc.)
                return prereq_status, prereq_result or {
                    "message": "Unknown error in prerequisite check",
                    "ability_id": ability_id
                }
            
        except Exception as e:
            logger.error(f"Failed to set ability {ability_id} for character id {user_char_id}: {e}")
            return Constants.ERROR, {
                "message": f"Failed to set ability: {str(e)}",
                "ability_id": ability_id
            }