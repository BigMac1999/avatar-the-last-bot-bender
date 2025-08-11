from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class Enemy(Base):
    """
    SQLAlchemy model for the enemies table
    """
    __tablename__ = "enemies"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    enemy_hp = Column(Integer, nullable=False)
    enemy_attack = Column(Integer, nullable=False)
    level = Column(Integer, default=1)
    behavior_type = Column(String(100), nullable=False)
    element = Column(String(20), nullable=False, index=True)
    xp_drop = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint("element IN ('fire', 'water', 'earth', 'air', 'none')", name="check_element"),
        CheckConstraint("behavior_type IN ('aggressive', 'defensive', 'balanced', 'healer')", name="check_behavior_type"),
    )
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #Relationships to other models
    enemy_abilities = relationship("EnemyAbilities", back_populates="enemy")    