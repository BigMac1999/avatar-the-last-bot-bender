from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class UserCharacter(Base):
    """
    Junction table model for user_characters table.
    
    Key concept: Many-to-Many relationships
    - Users can have many characters
    - Characters can be owned by many users  
    - This junction table creates the connection
    - UniqueConstraint prevents duplicate user-character pairs
    """
    __tablename__ = "user_characters"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    
    current_hp = Column(Integer, nullable=False)
    current_attack = Column(Integer, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint to prevent duplicate user-character pairs
    __table_args__ = (
        UniqueConstraint('user_id', 'character_id', name='uq_user_character'),
    )
    
    # Relationships to parent tables
    user = relationship("User", back_populates="user_characters")
    character = relationship("Character", back_populates="user_characters")
    
    # Relationship to user character abilities (another junction table)
    user_character_abilities = relationship("UserCharacterAbility", back_populates="user_character")
    
    def __repr__(self):
        return f"<UserCharacter(id={self.id}, user_id={self.user_id}, character_id={self.character_id})>"