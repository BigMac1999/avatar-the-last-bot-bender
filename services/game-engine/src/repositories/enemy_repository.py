from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from utils.constants import Constants
from models.enemy import Enemy
from models.enemy_abilities import EnemyAbility
from utils.serializers import Serializer

class EnemyRepository:
    """
    Repository for enemy-related database operations using SQLAlchemy ORM.
    """
    
    serializer = Serializer()
    
    async def get_all_enemies(self) -> tuple[Constants, Optional[List[dict]]]:
        """
        Get all enemies, returning serialized dictionaries
        """
        with database_manager.get_db_session() as session:
            enemies = session.query(Enemy).all()
            
            if not enemies:
                return Constants.INTERNAL_SERVER_ERROR, None
            
            return Constants.SUCCESS, [self.serializer.serialize_enemy(enemy) for enemy in enemies]
        
        return Constants.ERROR, None
    
    async def get_enemies_roster(self) -> tuple[Constants, Optional[List[dict]]]:
        """
        Get list of enemies and their abilities
        """
        with database_manager.get_db_session() as session:
            enemies = session.query(Enemy)\
                .options(joinedload(Enemy.enemy_abilities))\
                .all()
                
            if not enemies:
                return Constants.INTERNAL_SERVER_ERROR, None
            
            return Constants.SUCCESS, [self.serializer.serialize_enemy_with_abilities(enemy) for enemy in enemies]
        return Constants.ERROR, None
    
    async def get_single_enemy_details(self, enemy_id: int) -> tuple[Constants, Optional[dict]]:
        """
        Get details for a single enemy and their abilities
        """
        with database_manager.get_db_session() as session:
            enemy = session.query(Enemy)\
                .options(joinedload(Enemy.enemy_abilities))\
                .filter(Enemy.id == enemy_id)\
                .first()
                
            if not enemy:
                return Constants.NOT_FOUND, None
            
            return Constants.SUCCESS, self.serializer.serialize_enemy_with_abilities(enemy)