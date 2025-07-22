# from ..database.connection import database_manager
# from ..database.queries.users import GET_USER_BY_ID, GET_ALL_USERS, CREATE_USER

# class UserRepository:
#     """Repository for user-related database operations."""
    
#     async def get_user_by_id(self, user_id: int) -> dict:
#         """Fetch a user by their ID."""
#         with database_manager.get_db_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(GET_USER_BY_ID, (user_id,))
#             return cursor.fetchone()