from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class UserCharacterAbility(Base):
    """
    Junction table for user_character_abilities - tracks which abilities a user has unlocked for their characters.
    
    This represents a 3-way relationship:
    - User has Character (through UserCharacter)
    - Character can have Ability (through CharacterAbility) 
    - User unlocks specific Abilities for their Characters (this table)
    """
    __tablename__ = "user_character_abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_character_id = Column(Integer, ForeignKey("user_characters.id", ondelete="CASCADE"), nullable=False, index=True)
    ability_id = Column(Integer, ForeignKey("abilities.id", ondelete="CASCADE"), nullable=False, index=True)
    
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_character_id', 'ability_id', name='uq_user_character_ability'),
    )
    
    # Relationships
    user_character = relationship("UserCharacter", back_populates="user_character_abilities")
    ability = relationship("Ability", back_populates="user_character_abilities")
    
    def __repr__(self):
        return f"<UserCharacterAbility(user_character_id={self.user_character_id}, ability_id={self.ability_id})>"