from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from models.user_character_ability import UserCharacterAbility

class Serializer:
    """
    Helper methods used to serialize output from SQLAlchemy
    """
    
    def serialize_character(self, character: Character) -> dict:
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
        
    def serialize_user(self, user: User) -> dict:
        """Helper method to serialize a User object to dictionary"""
        return {
            "id": user.id,
            "discord_id": user.discord_id,
            "username": user.username,
            "created_at": user.created_at.isoformat() if user.created_at is not None else None
        }
    
    def serialize_user_character(self, userChar: UserCharacter) -> dict:
        """Helper method to serialize a UserCharacter object to dictionary"""
        return {
            "id": userChar.id,
            "user_id": userChar.user_id,
            "character_id": userChar.character_id,
            "current_hp": userChar.current_hp,
            "current_attack": userChar.current_attack,
            "level": userChar.level,
            "experience": userChar.experience,
            "created_at": userChar.created_at
        }
        
    def serialize_user_roster(self, userChar: UserCharacter) -> dict:
        """Helper method to serialize the roster to a dictionary"""
        return {
            "id": userChar.id,
            "user_id": userChar.user_id,
            "character_id": userChar.character_id,

            # Character base info
            "name": userChar.character.name,
            "element": userChar.character.element,
            "rarity": userChar.character.rarity,
            "description": userChar.character.description,

            # User-specific stats (current instance)
            "current_hp": userChar.current_hp,
            "current_attack": userChar.current_attack,
            "level": userChar.level,
            "experience": userChar.experience,

            # Base stats for reference (optional)
            "base_hp": userChar.character.hp,
            "base_attack": userChar.character.attack,

            "created_at": userChar.created_at
        }
        
    def serialize_user_character_ability(self, userCharAbility: UserCharacterAbility) -> dict:
        """Helper method to serialize the user character ability to a dictionary"""
        return {
            "id": userCharAbility.id,
            "user_character_id": userCharAbility.user_character_id,
            "ability_id": userCharAbility.ability_id,
            "unlocked_at": userCharAbility.unlocked_at,
            
            #Ability info
            "name": userCharAbility.ability.name,
            "description": userCharAbility.ability.description,
            "attack": userCharAbility.ability.attack,
            "defense": userCharAbility.ability.defense,
            "element": userCharAbility.ability.element.capitalize(),
        }
        