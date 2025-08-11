from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint, String
from sqlalchemy.orm import relationship
from database.connection import Base

class EnemyAbility(Base):
    """
    Junction table for enemy_abilities - which abilities each enemy can have.
    
    This is a simple many-to-many relationship:
    - Enemies can have many abilities
    - Abilities can belong to many enemies
    """
    __tablename__ = "enemy_abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    enemy_id = Column(Integer, ForeignKey("enemies.id", ondelete="CASCADE"), nullable=False, index=True)
    ability_id = Column(Integer, ForeignKey("abilities.id", ondelete="CASCADE"), nullable=False, index=True)
    behavior_type = Column(String(100), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('enemy_id', 'ability_id', name='uq_enemy_ability'),
        CheckConstraint("behavior_type IN ('aggressive', 'defensive', 'balanced', 'healer')", name="check_behavior_type"),
    )
    
    # Relationships
    enemy = relationship("Enemy", back_populates="enemy_abilities")
    ability = relationship("Ability", back_populates="enemy_abilities")