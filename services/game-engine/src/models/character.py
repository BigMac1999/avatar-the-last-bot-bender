from sqlalchemy import Column, Integer, String, Text, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class Character(Base):
    """
    SQLAlchemy model for the characters table.
    
    New concepts here:
    - CheckConstraint: Enforces database-level constraints (like element choices)
    - Text: For longer text fields (vs String for shorter VARCHAR)
    - Indexes are defined in Column() with index=True
    """
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    
    # Element with constraint check - must be one of the allowed values
    element = Column(String(20), nullable=False, index=True)
    __table_args__ = (
        CheckConstraint("element IN ('fire', 'water', 'earth', 'air', 'none')", name="check_element"),
        CheckConstraint("rarity IN (1, 2, 3)", name="check_rarity"),
        CheckConstraint("hp > 0", name="check_hp_positive"),
        CheckConstraint("attack > 0", name="check_attack_positive")
    )
    
    rarity = Column(Integer, nullable=False, index=True)
    hp = Column(Integer, nullable=False)  
    attack = Column(Integer, nullable=False)
    description = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships to other models
    user_characters = relationship("UserCharacter", back_populates="character")
    character_abilities = relationship("CharacterAbility", back_populates="character")
    
    # Property to get abilities through the junction table
    @property
    def abilities(self):
        """Get all abilities for this character"""
        return [ca.ability for ca in self.character_abilities]
    
    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}', element='{self.element}', rarity={self.rarity})>"