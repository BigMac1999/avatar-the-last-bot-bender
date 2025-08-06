from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability

class CharacterRepository:
    """
    Repository for character-related database operations using SQLAlchemy ORM.
    """
    
    def _serialize_character(self, character: Character) -> dict:
        """Helper method to serialize a Character object to dictionary"""
        return {
            "id": character.id,
            "name": character.name,
            "element": character.element,
            "rarity": character.rarity,
            "hp": character.hp,
            "attack": character.attack,
            "description": character.description,
            "created_at": character.created_at.isoformat() if character.created_at is not None else None
        }
    
    async def get_all_characters(self) -> List[dict]:
        """
        Get all characters from database, returning serialized dictionaries.
        
        Old way: cursor.execute("SELECT * FROM characters")
        New way: session.query(Character).all()
        
        Benefits:
        - Returns Python objects instead of tuples
        - Automatic type conversion
        - IDE autocomplete and type checking
        - Serialized while session is active
        """
        with database_manager.get_db_session() as session:
            characters = session.query(Character).all()
            
            # Serialize all characters while session is active
            return [self._serialize_character(char) for char in characters]
    
    async def get_character_by_name(self, character_name: str) -> Optional[dict]:
        """
        Get character by name, returning a dictionary for JSON serialization.
        
        Old way: "SELECT * FROM characters WHERE name = %s"
        New way: session.query(Character).filter(Character.name == character_name).first()
        
        Benefits:
        - No SQL injection risks (automatic parameter binding)
        - Column names are checked at development time
        - Returns None instead of empty result
        - Serializes to dict while session is active (avoids DetachedInstanceError)
        """
        with database_manager.get_db_session() as session:
            character = session.query(Character).filter(Character.name == character_name).first()
            if not character:
                return None
            
            # Serialize while session is active
            return self._serialize_character(character)
    
    async def get_character_by_id(self, character_id: int) -> Optional[dict]:
        """Get character by ID - demonstrates primary key lookup."""
        with database_manager.get_db_session() as session:
            # .get() is shorthand for primary key lookup
            character = session.get(Character, character_id)
            if not character:
                return None
            return self._serialize_character(character)
    
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
            return [self._serialize_character(char) for char in characters]
    
    async def get_character_with_abilities(self, character_id: int) -> Optional[dict]:
        """
        Get character with all their abilities loaded.
        
        Key concept: Eager Loading
        - joinedload() prevents N+1 query problem
        - Loads related data in single query instead of multiple
        - Old way would require separate queries or complex JOINs
        """
        with database_manager.get_db_session() as session:
            character = session.query(Character)\
                .options(joinedload(Character.character_abilities))\
                .filter(Character.id == character_id)\
                .first()
            
            if not character:
                return None
                
            # Serialize character with abilities
            char_data = self._serialize_character(character)
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
        
                        # .options(joinedload(Character.character_abilities).joinedload(Character.abilities))\

    
    async def create_character(self, name: str, element: str, rarity: int, hp: int, attack: int, description: str = "") -> dict:
        """
        Create new character.
        
        Old way: "INSERT INTO characters (...) VALUES (...) RETURNING *"
        New way: Create object, add to session, commit
        
        Benefits:
        - Validation happens in Python (model constraints)
        - Object is immediately usable after creation
        - Relationships can be set up easily
        """
        with database_manager.get_db_session() as session:
            character = Character(
                name=name,
                element=element, 
                rarity=rarity,
                hp=hp,
                attack=attack,
                description=description
            )
            session.add(character)
            session.flush()  # Get the ID without committing
            session.refresh(character)  # Refresh to get generated fields
            return self._serialize_character(character)
    
    async def update_character(self, character_id: int, **updates) -> Optional[dict]:
        """
        Update character fields.
        
        Demonstrates partial updates using **kwargs
        """
        with database_manager.get_db_session() as session:
            character = session.get(Character, character_id)
            if not character:
                return None
            
            # Update only provided fields
            for field, value in updates.items():
                if hasattr(character, field):
                    setattr(character, field, value)
            
            session.flush()
            session.refresh(character)
            return self._serialize_character(character)
    
    async def delete_character(self, character_id: int) -> bool:
        """Delete character by ID."""
        with database_manager.get_db_session() as session:
            character = session.get(Character, character_id)
            if not character:
                return False
            
            session.delete(character)
            return True