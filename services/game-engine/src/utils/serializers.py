from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from models.user_character_ability import UserCharacterAbility
from models.ability_prerequisite import AbilityPrerequisite

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
        
    def serialize_ability(self, ability: Ability) -> dict:
        """Helper method to serialize the ability to a dictionary"""
        return {
            "id": ability.id,
            "name": ability.name,
            "description": ability.description,
            "attack": ability.attack,
            "defense": ability.defense,
            "element": ability.element.capitalize(),
        }
        
    def serialize_ability_prereq(self, abilityPrereq: AbilityPrerequisite) -> dict:
        """Helper method to serialize the ability prerequisite to a dictionary"""
        return {
            "id": abilityPrereq.id,
            "ability_id": abilityPrereq.ability_id,
            "ability_name":abilityPrereq.ability.name,
            "ability_description":abilityPrereq.ability.description,
            "ability_attack": abilityPrereq.ability.attack,
            "ability_defense": abilityPrereq.ability.defense,
            "ability_element": abilityPrereq.ability.element,
            "ability_unlock_cost": abilityPrereq.ability.unlock_cost,
            "prerequisite_ability_id": abilityPrereq.prerequisite_ability_id,
            "prerequisite_ability_name":abilityPrereq.prerequisite_ability.name,
            "prerequisite_ability_description":abilityPrereq.prerequisite_ability.description,
            "prerequisite_ability_attack": abilityPrereq.prerequisite_ability.attack,
            "prerequisite_ability_defense": abilityPrereq.prerequisite_ability.defense,
            "prerequisite_ability_element": abilityPrereq.prerequisite_ability.element,
            "prerequisite_ability_unlock_cost": abilityPrereq.prerequisite_ability.unlock_cost,
        }