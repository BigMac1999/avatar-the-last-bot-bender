from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class CharacterAbility(Base):
    """
    Junction table for characters_abilities - which abilities each character can have.
    
    This is a simple many-to-many relationship:
    - Characters can have many abilities
    - Abilities can belong to many characters
    """
    __tablename__ = "characters_abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False, index=True)
    ability_id = Column(Integer, ForeignKey("abilities.id", ondelete="CASCADE"), nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint('character_id', 'ability_id', name='uq_character_ability'),
    )
    
    # Relationships
    character = relationship("Character", back_populates="character_abilities")
    ability = relationship("Ability", back_populates="character_abilities")
    
    def __repr__(self):
        return f"<CharacterAbility(character_id={self.character_id}, ability_id={self.ability_id})>"