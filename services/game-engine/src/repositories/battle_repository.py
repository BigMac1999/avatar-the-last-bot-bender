from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from utils.constants import Constants
from models.battle import Battle
from utils.serializers import Serializer
from models.enemy import Enemy


class BattleRepository:
    """
    Repository for battle-related database operations using SQLAlchemy ORM.
    """
    
    serializer = Serializer()
    
    async def get_battle(self, battle_id: int) -> tuple[Constants, Optional[dict]]:
        """Get a battle from Postgres"""
        with database_manager.get_db_session() as session:
            battle = session.query(Battle)\
                .filter(Battle.id == battle_id)\
                .first()
            
            if not battle: 
                return Constants.NOT_FOUND, None
            
            return Constants.SUCCESS, self.serializer.serialize_battle(battle)

    
    async def create_battle_request_user(self, user_id: int, opponent_id: int, battle_type: str = "user"):
        """
        Create a new battle between user_id (requestor) and opponent_id (requestee)
        """
        with database_manager.get_db_session() as session:
            opponent_check = session.query(User).filter(User.discord_id == opponent_id).first()
            
            if not opponent_check:
                return Constants.NOT_FOUND, None
            
            prior_battle = session.query(Battle)\
                .filter(Battle.challenger_id == user_id,
                        Battle.opponent_id == opponent_id,
                        Battle.status == "pending")\
                .first()
                
            if prior_battle:
                return Constants.ALREADY_EXISTS, None 
            
            battle = Battle(
                challenger_id=user_id,
                opponent_id=opponent_id,
                battle_type=battle_type,
                status="pending"
            )
            session.add(battle)
            session.commit()
            session.refresh(battle)
            
            return Constants.SUCCESS, self.serializer.serialize_battle(battle)
        return Constants.ERROR, None
        
    async def create_battle_bot(self, user_id: int, opponent_id: int, battle_type: str = "bot"):
        """
        Create a new battle between a user and a bot
        """
        with database_manager.get_db_session() as session:
            enemy = session.query(Enemy).filter(Enemy.id == opponent_id)
            
            if not enemy:
                return Constants.NOT_FOUND, None
            
            battle = Battle(
                challenger_id=user_id,
                opponent_id=opponent_id,
                battle_type=battle_type,
                status="pending"
            )
            session.add(battle)
            session.commit()
            session.refresh(battle)
            
            return Constants.SUCCESS, self.serializer.serialize_battle(battle)
        return Constants.ERROR, None
    
    async def update_battle(self, battle_id: int, **updates) -> tuple[Constants, Optional[dict]]:
        """
        Update battle in postgres
        """
        with database_manager.get_db_session() as session:
            battle = session.query(Battle)\
                .filter(Battle.id == battle_id)\
                .first()
                
            if not battle:
                return Constants.NOT_FOUND, None
            
            for field, value in updates.items():
                if hasattr(battle, field):
                    setattr(battle, field, value)
                else:
                    return Constants.BAD_REQUEST, None
                
            session.commit()
            session.refresh(battle)
            
            return Constants.SUCCESS, battle