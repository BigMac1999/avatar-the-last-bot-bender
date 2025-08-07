from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from utils.constants import Constants
from utils.serializers import Serializer

class CharacterRepository:
    """
    Repository for character-related database operations using SQLAlchemy ORM.
    """
    
    serializer = Serializer()
    
    async def get_all_characters(self) -> List[dict]:
        """
        Get all characters from database, returning serialized dictionaries.
        """
        with database_manager.get_db_session() as session:
            characters = session.query(Character).all()
            
            # Serialize all characters while session is active
            return [self.serializer.serialize_character(char) for char in characters]
    
    async def get_character_by_name(self, character_name: str) -> Optional[dict]:
        """
        Get character by name, returning a dictionary for JSON serialization.
        """
        with database_manager.get_db_session() as session:
            character = session.query(Character).filter(Character.name == character_name).first()
            if not character:
                return None
            
            # Serialize while session is active
            return self.serializer.serialize_character(character)
    
    async def get_character_by_id(self, character_id: int) -> Optional[dict]:
        """Get character by ID - demonstrates primary key lookup."""
        with database_manager.get_db_session() as session:
            # .get() is shorthand for primary key lookup
            character = session.get(Character, character_id)
            if not character:
                return None
            return self.serializer.serialize_character(character)
    
    async def get_characters_by_element(self, element: str) -> List[dict]:
        """
        Get all characters of a specific element.
        Demonstrates filtering with WHERE clause equivalent.
        """
        with database_manager.get_db_session() as session:
            characters = session.query(Character)\
                .filter(Character.element == element)\
                .order_by(Character.rarity.desc(), Character.name)\
                .all()
            return [self.serializer.serialize_character(char) for char in characters]
    
    async def get_character_with_abilities(self, character_id: int) -> Optional[dict]:
        """
        Get character with all their abilities loaded.
        """
        with database_manager.get_db_session() as session:
            character = session.query(Character)\
                .options(joinedload(Character.character_abilities))\
                .filter(Character.id == character_id)\
                .first()
            
            if not character:
                return None
                
            # Serialize character with abilities
            char_data = self.serializer.serialize_character(character)
            char_data["abilities"] = [
                {
                    "id": ca.ability.id,
                    "name": ca.ability.name,
                    "description": ca.ability.description,
                    "attack": ca.ability.attack,
                    "defense": ca.ability.defense,
                    "element": ca.ability.element,
                    "unlock_cost": ca.ability.unlock_cost
                }
                for ca in character.character_abilities
            ]
            return char_data
        
        
    async def get_users_characters(self, user_id: int) -> tuple[Constants, Optional[List[dict]]]:
        """
        Get all characters claimed by a single user
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if not user:
                return Constants.USER_NOT_FOUND, None
            
            user_characters = session.query(UserCharacter)\
                .filter(UserCharacter.user_id == user.id)\
                .all()
                
            if not user_characters:
                return Constants.NOT_FOUND, None
            
            return Constants.SUCCESS, [self.serializer.serialize_user_character(user_char) for user_char in user_characters]
        
    async def get_users_roster(self, user_id: int) -> tuple[Constants, Optional[List[dict]]]:
        """
        Get all characters and details claimed by a single user (their roster)
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if not user:
                return Constants.USER_NOT_FOUND, None
            
            characters = session.query(UserCharacter)\
                .options(joinedload(UserCharacter.character))\
                .filter(UserCharacter.user_id == user.id)\
                .all()
                                
            if not characters:
                return Constants.NOT_FOUND, None
            
            return Constants.SUCCESS, [self.serializer.serialize_user_roster(char) for char in characters]
                    
    async def set_character_to_user(self, user_id: int, character_id:int) -> tuple[Constants, Optional[dict]]:
        """
        Give a user claim to a character
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if not user:
                return Constants.USER_NOT_FOUND, None
            
            userChar = session.query(UserCharacter)\
                .filter(UserCharacter.user_id == user.id, 
                    UserCharacter.character_id == character_id)\
                .first()
            
            if userChar:
                return Constants.ALREADY_EXISTS, None

            baseChar = session.query(Character)\
                .filter(Character.id == character_id)\
                .first()
                
            if not baseChar:
                return Constants.NOT_FOUND, None
            
            userChar = UserCharacter(user_id=user.id, 
                                     character_id=character_id,
                                     current_hp=baseChar.hp,
                                     current_attack=baseChar.attack)
            session.add(userChar)
            session.commit()
            session.refresh(userChar)
            
            return Constants.SUCCESS, self.serializer.serialize_user_character(userChar)
            
    async def unset_character_to_user(self, user_id: int, character_id: int) -> tuple[Constants, Optional[dict]]:
        """
        Unset/Remove a character from a user
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if not user:
                return Constants.USER_NOT_FOUND, None
            
            userChar = session.query(UserCharacter)\
                .filter(UserCharacter.user_id == user.id, 
                    UserCharacter.character_id == character_id)\
                .first()
            
            if not userChar:
                return Constants.NOT_FOUND, None
            
            session.delete(userChar)
            return Constants.SUCCESS, userChar
        
    
        
        
        
        
        
        
        
        
        
        
        
        
    """These methods currently unused since we spin up db to often, this will be implemented post MVP"""
    # async def create_character(self, name: str, element: str, rarity: int, hp: int, attack: int, description: str = "") -> dict:
    #     """
    #     Create new character.
    #     """
    #     with database_manager.get_db_session() as session:
    #         character = Character(
    #             name=name,
    #             element=element, 
    #             rarity=rarity,
    #             hp=hp,
    #             attack=attack,
    #             description=description
    #         )
    #         session.add(character)
    #         session.flush()  # Get the ID without committing
    #         session.refresh(character)  # Refresh to get generated fields
    #         return self._serialize_character(character)
    
    # async def update_character(self, character_id: int, **updates) -> Optional[dict]:
    #     """
    #     Update character fields.
    #     """
    #     with database_manager.get_db_session() as session:
    #         character = session.get(Character, character_id)
    #         if not character:
    #             return None
            
    #         # Update only provided fields
    #         for field, value in updates.items():
    #             if hasattr(character, field):
    #                 setattr(character, field, value)
            
    #         session.flush()
    #         session.refresh(character)
    #         return self._serialize_character(character)
    
    # async def delete_character(self, character_id: int) -> bool:
    #     """Delete character by ID."""
    #     with database_manager.get_db_session() as session:
    #         character = session.get(Character, character_id)
    #         if not character:
    #             return False
            
    #         session.delete(character)
    #         return True