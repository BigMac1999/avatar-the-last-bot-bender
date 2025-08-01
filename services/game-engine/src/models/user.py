from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    """
    SQLAlchemy model for the users table.
    
    Key concepts:
    - Base: All models inherit from this declarative base
    - __tablename__: Maps this class to the 'users' database table  
    - Column: Defines database columns with types and constraints
    - relationship: Defines connections to other models (joins)
    """
    __tablename__ = "users"
    
    # Primary key - SQLAlchemy automatically handles SERIAL type
    id = Column(Integer, primary_key=True, index=True)
    
    # Discord ID - BigInteger for large Discord IDs, unique=True for constraint
    discord_id = Column(BigInteger, unique=True, nullable=False, index=True)
    
    # Username - String maps to VARCHAR, nullable=False means NOT NULL
    username = Column(String(255), nullable=False)
    
    # Timestamps - func.now() provides DEFAULT CURRENT_TIMESTAMP
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships - These create "virtual" attributes for related data
    # back_populates creates bidirectional relationships
    challenger_battles = relationship("Battle", foreign_keys="Battle.challenger_id", back_populates="challenger")
    opponent_battles = relationship("Battle", foreign_keys="Battle.opponent_id", back_populates="opponent") 
    won_battles = relationship("Battle", foreign_keys="Battle.winner_id", back_populates="winner")
    user_characters = relationship("UserCharacter", back_populates="user")
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<User(id={self.id}, username='{self.username}', discord_id={self.discord_id})>"