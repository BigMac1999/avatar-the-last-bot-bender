from sqlalchemy import Column, Integer, String, Text, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class Ability(Base):
    """SQLAlchemy model for the abilities table"""
    __tablename__ = "abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    element = Column(String(20), nullable=False, index=True)
    unlock_cost = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("element IN ('fire', 'water', 'earth', 'air', 'none')", name="check_ability_element"),
        CheckConstraint("attack >= 0", name="check_ability_attack"),
        CheckConstraint("unlock_cost >= 0", name="check_unlock_cost")
    )
    
    # Relationships
    character_abilities = relationship("CharacterAbility", back_populates="ability")
    enemy_abilities = relationship("EnemyAbility", back_populates="ability")
    user_character_abilities = relationship("UserCharacterAbility", back_populates="ability")
    prerequisites = relationship("AbilityPrerequisite", foreign_keys="AbilityPrerequisite.ability_id", back_populates="ability")
    required_for = relationship("AbilityPrerequisite", foreign_keys="AbilityPrerequisite.prerequisite_ability_id", back_populates="prerequisite_ability")
    
    def __repr__(self):
        return f"<Ability(id={self.id}, name='{self.name}', element='{self.element}', attack={self.attack})>"