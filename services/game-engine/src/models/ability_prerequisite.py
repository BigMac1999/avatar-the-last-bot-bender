from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class AbilityPrerequisite(Base):
    """
    Self-referencing table for ability_prerequisites - abilities that require other abilities.
    
    Key concept: Self-referencing relationships
    - An ability can require other abilities to be unlocked first
    - This creates a hierarchy/tree of ability dependencies
    - Both ability_id and prerequisite_ability_id reference the same abilities table
    """
    __tablename__ = "ability_prerequisites"
    
    id = Column(Integer, primary_key=True, index=True)
    ability_id = Column(Integer, ForeignKey("abilities.id", ondelete="CASCADE"), nullable=False, index=True)
    prerequisite_ability_id = Column(Integer, ForeignKey("abilities.id", ondelete="CASCADE"), nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint('ability_id', 'prerequisite_ability_id', name='uq_ability_prerequisite'),
    )
    
    # Self-referencing relationships - both point to Ability model
    ability = relationship("Ability", foreign_keys=[ability_id], back_populates="prerequisites")
    prerequisite_ability = relationship("Ability", foreign_keys=[prerequisite_ability_id], back_populates="required_for")
    
    def __repr__(self):
        return f"<AbilityPrerequisite(ability_id={self.ability_id}, prerequisite_ability_id={self.prerequisite_ability_id})>"