from typing import List, Optional
from sqlalchemy.orm import joinedload
from database.connection import database_manager
from models.user import User
from utils.constants import Constants
from utils.serializers import Serializer

class UserRepository:
    """
    Repository for user-related database operations using SQLAlchemy ORM.
    """
    
    serializer = Serializer()
    
    # Helper methods
        
    async def validate_user(self, user_id: int) -> bool:
        """
        Validate if a user exists by ID.
        Returns True if user exists, False otherwise.
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            return True if user else False
        
    # Getter methods
    
    async def get_all_users(self) -> List[dict]:
        """
        Get all users from the database, returning serialized dictionaries.
        """
        with database_manager.get_db_session() as session:
            users = session.query(User).all()
            
            return [self.serializer.serialize_user(user) for user in users]
        return []  # Return an empty list if no users found
    
    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """
        Get User by ID, returning a dictionary for JSON serialization.
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter(User.discord_id == user_id).first()
            
            return self.serializer.serialize_user(user) if user else None
    
    # Setter Methods
    
    async def onboard_user(self, user_id: int, username: str = "User") -> tuple[Constants, Optional[dict]]:
        """
        Onboard a new user to the game, also letting us know if the user already exists.
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if user:
                return Constants.ALREADY_EXISTS, None

            user = User(discord_id=user_id, username=username)
            session.add(user)
            session.commit()
            session.refresh(user)
            return Constants.CREATED, self.serializer.serialize_user(user)
            
    async def update_username_by_id(self, user_id: int, username: str):
        """
        Update an existing user's username.
        """
        with database_manager.get_db_session() as session:
            user = session.query(User).filter_by(discord_id=user_id).first()
            if user: 
                user = session.query(User).filter_by(discord_id=user_id).update({"username": username})
                return Constants.SUCCESS
            return Constants.NOT_FOUND
        return Constants.INTERNAL_SERVER_ERROR
    
    