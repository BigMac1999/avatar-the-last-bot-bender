# from typing import List, Optional
# from datetime import datetime
# from sqlalchemy.orm import joinedload
# from sqlalchemy import and_, or_, func, desc
# from database.connection import database_manager
# from models.battle import Battle
# from models.user import User

# class BattleRepository:
#     """
#     Repository for battle-related database operations.
    
#     Advanced ORM concepts demonstrated:
#     - Complex queries with multiple conditions
#     - Aggregation functions (COUNT, etc.)
#     - Subqueries and joins
#     - Date/time handling
#     """
    
#     async def get_battle_by_id(self, battle_id: int) -> Optional[Battle]:
#         """Get battle with all related user data loaded."""
#         with database_manager.get_db_session() as session:
#             battle = session.query(Battle)\
#                 .options(
#                     joinedload(Battle.challenger),
#                     joinedload(Battle.opponent), 
#                     joinedload(Battle.winner)
#                 )\
#                 .filter(Battle.id == battle_id)\
#                 .first()
#             return battle
    
#     async def get_user_battles(self, user_id: int, limit: int = 50) -> List[Battle]:
#         """
#         Get all battles for a user (as challenger or opponent).
        
#         Demonstrates: OR conditions, ordering, limiting
#         """
#         with database_manager.get_db_session() as session:
#             battles = session.query(Battle)\
#                 .filter(
#                     or_(
#                         Battle.challenger_id == user_id,
#                         Battle.opponent_id == user_id
#                     )
#                 )\
#                 .order_by(desc(Battle.created_at))\
#                 .limit(limit)\
#                 .all()
#             return battles
    
#     async def get_user_battle_stats(self, user_id: int) -> dict:
#         """
#         Get battle statistics for a user.
        
#         Advanced concept: Aggregation queries
#         - COUNT() function
#         - Conditional counting with CASE/WHEN equivalent
#         - Multiple aggregates in single query
#         """
#         with database_manager.get_db_session() as session:
#             # Total battles participated in
#             total_battles = session.query(func.count(Battle.id))\
#                 .filter(
#                     or_(
#                         Battle.challenger_id == user_id,
#                         Battle.opponent_id == user_id
#                     )
#                 ).scalar()
            
#             # Battles won
#             battles_won = session.query(func.count(Battle.id))\
#                 .filter(Battle.winner_id == user_id)\
#                 .scalar()
            
#             # Battles as challenger
#             as_challenger = session.query(func.count(Battle.id))\
#                 .filter(Battle.challenger_id == user_id)\
#                 .scalar()
            
#             # Recent battles (last 30 days)
#             thirty_days_ago = datetime.now() - datetime.timedelta(days=30)
#             recent_battles = session.query(func.count(Battle.id))\
#                 .filter(
#                     and_(
#                         or_(
#                             Battle.challenger_id == user_id,
#                             Battle.opponent_id == user_id
#                         ),
#                         Battle.created_at >= thirty_days_ago
#                     )
#                 ).scalar()
            
#             return {
#                 "total_battles": total_battles or 0,
#                 "battles_won": battles_won or 0,
#                 "battles_lost": (total_battles or 0) - (battles_won or 0),
#                 "win_rate": (battles_won / total_battles * 100) if total_battles > 0 else 0,
#                 "as_challenger": as_challenger or 0,
#                 "recent_battles": recent_battles or 0
#             }
    
#     async def create_battle(self, challenger_id: int, opponent_id: int, battle_log: str = None) -> Battle:
#         """
#         Create a new battle.
        
#         Demonstrates: Object creation with relationships
#         """
#         with database_manager.get_db_session() as session:
#             battle = Battle(
#                 challenger_id=challenger_id,
#                 opponent_id=opponent_id,
#                 battle_log=battle_log,
#                 status="pending"
#             )
#             session.add(battle)
#             session.flush()
#             session.refresh(battle)
#             return battle
    
#     async def complete_battle(self, battle_id: int, winner_id: int, battle_log: str) -> Optional[Battle]:
#         """
#         Complete a battle by setting winner and final battle log.
        
#         Demonstrates: Updates with validation
#         """
#         with database_manager.get_db_session() as session:
#             battle = session.get(Battle, battle_id)
#             if not battle:
#                 return None
            
#             # Validate winner is one of the participants
#             if winner_id not in [battle.challenger_id, battle.opponent_id]:
#                 raise ValueError("Winner must be either challenger or opponent")
            
#             battle.winner_id = winner_id
#             battle.battle_log = battle_log
#             battle.status = "completed"
#             battle.completed_at = datetime.now()
            
#             session.flush()
#             session.refresh(battle)
#             return battle
    
#     async def get_pending_battles(self, user_id: int = None) -> List[Battle]:
#         """
#         Get pending battles, optionally filtered by user.
        
#         Demonstrates: Optional filtering
#         """
#         with database_manager.get_db_session() as session:
#             query = session.query(Battle)\
#                 .options(
#                     joinedload(Battle.challenger),
#                     joinedload(Battle.opponent)
#                 )\
#                 .filter(Battle.status == "pending")
            
#             if user_id:
#                 query = query.filter(
#                     or_(
#                         Battle.challenger_id == user_id,
#                         Battle.opponent_id == user_id
#                     )
#                 )
            
#             battles = query.order_by(Battle.created_at).all()
#             return battles
    
#     async def get_battle_leaderboard(self, limit: int = 10) -> List[dict]:
#         """
#         Get top players by win count.
        
#         Advanced concept: Joins with aggregation
#         - JOIN users table with battles  
#         - GROUP BY user
#         - ORDER BY win count
#         """
#         with database_manager.get_db_session() as session:
#             # This is equivalent to a complex SQL query with JOINs and GROUP BY
#             results = session.query(
#                 User.id,
#                 User.username,
#                 func.count(Battle.id).label('wins')
#             )\
#             .join(Battle, Battle.winner_id == User.id)\
#             .group_by(User.id, User.username)\
#             .order_by(desc('wins'))\
#             .limit(limit)\
#             .all()
            
#             # Convert to dict format
#             leaderboard = []
#             for user_id, username, wins in results:
#                 leaderboard.append({
#                     "user_id": user_id,
#                     "username": username, 
#                     "wins": wins
#                 })
            
#             return leaderboard