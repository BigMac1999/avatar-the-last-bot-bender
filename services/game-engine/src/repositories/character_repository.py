import database.queries.characters 
from database.connection import database_manager

class CharacterRepository:
    """Repository for character-related database operations."""
    
    async def get_all_characters(self):
        with database_manager.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(database.queries.characters.GET_ALL_CHARACTERS)
            return cursor.fetchall()
        
    async def get_character_by_id(self, character_name: str):
        with database_manager.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE name = %s",(character_name,))
            return cursor.fetchone()