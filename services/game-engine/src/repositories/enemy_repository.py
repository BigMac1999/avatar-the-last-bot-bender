from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.character import Character
from models.ability import Ability
from models.user import User
from models.user_character import UserCharacter
from utils.constants import Constants
from utils.serializers import Serializer

class EnemyRepository:
    """
    Repository for enemy-related database operations using SQLAlchemy ORM.
    """
    
    serializer = Serializer()