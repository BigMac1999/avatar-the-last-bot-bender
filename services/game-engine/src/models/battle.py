from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class Battle(Base):
    """
    SQLAlchemy model for the battles table.
    
    New concepts:
    - ForeignKey: Creates references to other tables (like REFERENCES in SQL)
    - Multiple foreign keys to the same table (challenger, opponent, winner)
    - foreign_keys parameter in relationship() to specify which FK to use
    """
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys to users table - notice how we handle multiple references
    challenger_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    opponent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  
    winner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    battle_log = Column(Text)  # JSON string of battle events
    status = Column(String(20), default="completed", index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'cancelled')", name="check_battle_status"),
    )
    
    # Relationships - Notice foreign_keys parameter to handle multiple FKs to same table
    challenger = relationship("User", foreign_keys=[challenger_id], back_populates="challenger_battles")
    opponent = relationship("User", foreign_keys=[opponent_id], back_populates="opponent_battles")
    winner = relationship("User", foreign_keys=[winner_id], back_populates="won_battles")
    
    def __repr__(self):
        return f"<Battle(id={self.id}, challenger_id={self.challenger_id}, opponent_id={self.opponent_id}, status='{self.status}')>"