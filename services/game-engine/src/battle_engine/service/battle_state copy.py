import json
import logging
from typing import Optional, Dict, Any, List
from database.connection import redis_manager

logger = logging.getLogger(__name__)

"""
Battle State

Handles Redis operations for real-time battle state persistence and retrieval.
Manages temporary battle data during active combat sessions.
"""


class BattleState:
    
    def __init__(self):
        self.redis_manager = redis_manager  # Use global Redis manager
        # Key prefixes help organize data and avoid naming conflicts
        self.key_prefix = "battle"
    
    def _get_battle_key(self, battle_id: int, suffix: str = "") -> str:
        """
        Generate consistent Redis keys for battle data
        
        Redis keys are like file paths - they should be consistent and organized
        Examples:
        - battle:123:state
        - battle:123:participants
        - battle:123:events
        """
        base_key = f"{self.key_prefix}:{battle_id}"
        return f"{base_key}:{suffix}" if suffix else base_key
    
    async def create_battle_state(self, battle_id: int, state_data: Dict[str, Any]) -> bool:
        """
        Create battle state for future battle
        """
        try: 
            redis_conn = await self.redis_manager.create_connection()
            try:
                pass
            finally:
                pass
        except Exception:
            pass
    
    # async def set_battle_state(self, battle_id: int, state_data: Dict[str, Any], ttl: int = 1800) -> bool:
    #     """
    #     Store complete battle state in Redis
        
    #     Args:
    #         battle_id: Unique battle identifier
    #         state_data: Python dictionary containing battle state
    #         ttl: Time To Live in seconds (1800 = 30 minutes)
            
    #     Returns:
    #         True if successful, False otherwise
            
    #     Redis Concepts:
    #     - JSON serialization: Convert Python dict to JSON string for storage
    #     - TTL: Automatic expiration prevents Redis from filling up with old data
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, "state")
                
    #             # Convert Python dictionary to JSON string
    #             # Redis stores strings, not Python objects
    #             json_data = json.dumps(state_data)
                
    #             # Store with expiration time (TTL)
    #             # setex = SET with EXpiration
    #             await redis_conn.setex(key, ttl, json_data)
                
    #             logger.debug(f"Stored battle state for battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to store battle state for battle {battle_id}: {e}")
    #         return False
    
    # async def get_battle_state(self, battle_id: int) -> Optional[Dict[str, Any]]:
    #     """
    #     Retrieve battle state from Redis
        
    #     Returns:
    #         Dictionary containing battle state, or None if not found/error
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, "state")
                
    #             # Get JSON string from Redis
    #             json_data = await redis_conn.get(key)
                
    #             if json_data is None:
    #                 logger.debug(f"No battle state found for battle {battle_id}")
    #                 return None
                
    #             # Convert JSON string back to Python dictionary
    #             # Redis returns string due to decode_responses=True
    #             state_data = json.loads(str(json_data))
    #             logger.debug(f"Retrieved battle state for battle {battle_id}")
    #             return state_data
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve battle state for battle {battle_id}: {e}")
    #         return None
    
    # async def delete_battle_state(self, battle_id: int) -> bool:
    #     """
    #     Remove battle state from Redis (cleanup after battle ends)
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, "state")
                
    #             # Delete the key - returns number of keys deleted
    #             deleted_count = await redis_conn.delete(key)
                
    #             if deleted_count > 0:
    #                 logger.debug(f"Deleted battle state for battle {battle_id}")
    #                 return True
    #             else:
    #                 logger.debug(f"No battle state to delete for battle {battle_id}")
    #                 return False
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to delete battle state for battle {battle_id}: {e}")
    #         return False
    
    # async def set_participant_data(self, battle_id: int, participant_id: int, participant_data: Dict[str, Any]) -> bool:
    #     """
    #     Store participant data using Redis Hash
        
    #     Redis Hashes are perfect for storing object-like data (like participant info)
    #     Instead of storing everything as JSON, we can store individual fields
        
    #     Benefits of Redis Hashes:
    #     - Can update individual fields without rewriting entire object
    #     - More memory efficient for structured data
    #     - Built-in commands for hash operations
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"participant:{participant_id}")
                
    #             # Convert nested objects to JSON, keep simple values as-is
    #             hash_data = {}
    #             for field, value in participant_data.items():
    #                 if isinstance(value, (dict, list)):
    #                     # Complex data structures need to be JSON serialized
    #                     hash_data[field] = json.dumps(value)
    #                 else:
    #                     # Simple values can be stored directly
    #                     hash_data[field] = str(value)
                
    #             # Store as Redis hash with TTL
    #             # hset = Hash SET (set multiple hash fields at once)
    #             await redis_conn.hset(key, mapping=hash_data)  # type: ignore
    #             await redis_conn.expire(key, 1800)  # Set TTL separately for hashes
                
    #             logger.debug(f"Stored participant {participant_id} data for battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to store participant data: {e}")
    #         return False
    
    # async def add_battle_event(self, battle_id: int, event_data: Dict[str, Any]) -> bool:
    #     """
    #     Add event to battle event log using Redis Lists
        
    #     Redis Lists are perfect for:
    #     - Event logs (append-only)
    #     - Action queues
    #     - History tracking
        
    #     Lists maintain order and support efficient push/pop operations
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, "events")
                
    #             # Add timestamp to event
    #             import time
    #             event_data['timestamp'] = time.time()
                
    #             # Convert to JSON and add to list
    #             event_json = json.dumps(event_data)
                
    #             # lpush = Left PUSH (add to beginning of list)
    #             # rpush = Right PUSH (add to end of list)
    #             # We use rpush to maintain chronological order
    #             await redis_conn.rpush(key, event_json)  # type: ignore
                
    #             # Set TTL if this is the first event (key didn't exist)
    #             await redis_conn.expire(key, 1800)
                
    #             logger.debug(f"Added event to battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to add battle event: {e}")
    #         return False
    
    # async def get_battle_events(self, battle_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    #     """
    #     Get recent battle events using Redis List operations
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, "events")
                
    #             # lrange = List RANGE (get slice of list)
    #             # -limit to -1 gets the last 'limit' items
    #             event_strings = await redis_conn.lrange(key, -limit, -1)  # type: ignore
                
    #             # Convert JSON strings back to Python objects
    #             events = []
    #             for event_str in event_strings:
    #                 try:
    #                     event_data = json.loads(event_str)
    #                     events.append(event_data)
    #                 except json.JSONDecodeError:
    #                     logger.warning(f"Invalid JSON in battle event: {event_str}")
    #                     continue
                
    #             logger.debug(f"Retrieved {len(events)} events for battle {battle_id}")
    #             return events
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve battle events: {e}")
    #         return []
    
    # async def execute_battle_transaction(self, battle_id: int, updates: Dict[str, Any]) -> bool:
    #     """
    #     Execute multiple Redis operations atomically using transactions
        
    #     Redis Transactions (MULTI/EXEC):
    #     - Group multiple commands together
    #     - Execute all commands atomically (all succeed or all fail)
    #     - Prevent race conditions in concurrent environments
        
    #     Example use case: When a player makes a move, we need to:
    #     1. Update battle state
    #     2. Add event to log  
    #     3. Update participant data
    #     4. Set battle as modified
        
    #     All of these should happen together or not at all.
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             # Start Redis transaction
    #             # pipeline() creates a transaction context
    #             pipe = redis_conn.pipeline()
                
    #             # Add commands to transaction (they don't execute yet)
                
    #             # 1. Update battle state
    #             if 'state' in updates:
    #                 state_key = self._get_battle_key(battle_id, "state")
    #                 state_json = json.dumps(updates['state'])
    #                 pipe.setex(state_key, 1800, state_json)
                
    #             # 2. Add event if provided
    #             if 'event' in updates:
    #                 event_key = self._get_battle_key(battle_id, "events")
    #                 event_data = updates['event']
    #                 import time
    #                 event_data['timestamp'] = time.time()
    #                 event_json = json.dumps(event_data)
    #                 pipe.rpush(event_key, event_json)
    #                 pipe.expire(event_key, 1800)
                
    #             # 3. Update participant data if provided
    #             if 'participants' in updates:
    #                 for participant_id, participant_data in updates['participants'].items():
    #                     participant_key = self._get_battle_key(battle_id, f"participant:{participant_id}")
                        
    #                     # Convert data for hash storage
    #                     hash_data = {}
    #                     for field, value in participant_data.items():
    #                         if isinstance(value, (dict, list)):
    #                             hash_data[field] = json.dumps(value)
    #                         else:
    #                             hash_data[field] = str(value)
                        
    #                     pipe.hset(participant_key, mapping=hash_data)
    #                     pipe.expire(participant_key, 1800)
                
    #             # 4. Set last modified timestamp
    #             modified_key = self._get_battle_key(battle_id, "modified")
    #             import time
    #             pipe.setex(modified_key, 1800, str(time.time()))
                
    #             # Execute all commands atomically
    #             # execute() runs all commands in the pipeline together
    #             results = await pipe.execute()
                
    #             logger.debug(f"Executed transaction for battle {battle_id} with {len(results)} operations")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to execute battle transaction: {e}")
    #         return False
    
    # async def get_active_battles_for_user(self, user_id: int) -> List[int]:
    #     """
    #     Get list of active battles for a user using Redis Sets
        
    #     Redis Sets are perfect for:
    #     - Storing unique items (no duplicates)
    #     - Fast membership testing
    #     - Set operations (union, intersection, difference)
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = f"active_battles:user:{user_id}"
                
    #             # smembers = Set MEMBERS (get all items in set)
    #             battle_ids_str = await redis_conn.smembers(key)  # type: ignore
                
    #             # Convert strings back to integers
    #             battle_ids = [int(bid) for bid in battle_ids_str]
                
    #             logger.debug(f"Found {len(battle_ids)} active battles for user {user_id}")
    #             return battle_ids
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to get active battles for user {user_id}: {e}")
    #         return []
    
    # async def add_user_to_active_battle(self, user_id: int, battle_id: int) -> bool:
    #     """
    #     Add user to active battles set
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = f"active_battles:user:{user_id}"
                
    #             # sadd = Set ADD (add item to set)
    #             await redis_conn.sadd(key, battle_id)  # type: ignore
    #             await redis_conn.expire(key, 7200)  # 2 hours TTL for active battle tracking
                
    #             logger.debug(f"Added user {user_id} to active battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to add user to active battle: {e}")
    #         return False
    
    # async def remove_user_from_active_battle(self, user_id: int, battle_id: int) -> bool:
    #     """
    #     Remove user from active battles set
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = f"active_battles:user:{user_id}"
                
    #             # srem = Set REMove (remove item from set)
    #             removed_count = await redis_conn.srem(key, battle_id)  # type: ignore
                
    #             if removed_count > 0:
    #                 logger.debug(f"Removed user {user_id} from active battle {battle_id}")
    #                 return True
    #             else:
    #                 logger.debug(f"User {user_id} was not in active battle {battle_id}")
    #                 return False
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to remove user from active battle: {e}")
    #         return False
    
    # async def set_team_data(self, battle_id: int, user_id: int, team_data: Dict[str, Any]) -> bool:
    #     """
    #     Store complete team composition for a user in battle
        
    #     Team data structure:
    #     {
    #         "active_character_id": 1,
    #         "characters": {
    #             "1": {"hp": 100, "mp": 50, "status_effects": []},
    #             "2": {"hp": 80, "mp": 30, "status_effects": ["burn"]},
    #             ...
    #         },
    #         "team_size": 3,
    #         "available_swaps": 2
    #     }
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}")
                
    #             # Convert team data to JSON
    #             team_json = json.dumps(team_data)
    #             await redis_conn.setex(key, 1800, team_json)
                
    #             logger.debug(f"Stored team data for user {user_id} in battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to store team data for user {user_id}: {e}")
    #         return False
    
    # async def get_team_data(self, battle_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    #     """
    #     Retrieve complete team data for a user
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}")
                
    #             team_json = await redis_conn.get(key)
    #             if team_json is None:
    #                 logger.debug(f"No team data found for user {user_id} in battle {battle_id}")
    #                 return None
                
    #             team_data = json.loads(str(team_json))
    #             logger.debug(f"Retrieved team data for user {user_id} in battle {battle_id}")
    #             return team_data
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve team data for user {user_id}: {e}")
    #         return None
    
    # async def set_character_in_team(self, battle_id: int, user_id: int, character_id: int, character_data: Dict[str, Any]) -> bool:
    #     """
    #     Update individual character data within a team using Redis Hash
        
    #     Key structure: battle:{battle_id}:team:{user_id}:character:{character_id}
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}:character:{character_id}")
                
    #             # Convert complex data to JSON, simple values as strings
    #             hash_data = {}
    #             for field, value in character_data.items():
    #                 if isinstance(value, (dict, list)):
    #                     hash_data[field] = json.dumps(value)
    #                 else:
    #                     hash_data[field] = str(value)
                
    #             await redis_conn.hset(key, mapping=hash_data)  # type: ignore
    #             await redis_conn.expire(key, 1800)
                
    #             logger.debug(f"Updated character {character_id} for user {user_id} in battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to update character {character_id} for user {user_id}: {e}")
    #         return False
    
    # async def get_character_in_team(self, battle_id: int, user_id: int, character_id: int) -> Optional[Dict[str, Any]]:
    #     """
    #     Get individual character data from team
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}:character:{character_id}")
                
    #             char_data = await redis_conn.hgetall(key)  # type: ignore
    #             if not char_data:
    #                 logger.debug(f"No character {character_id} found for user {user_id} in battle {battle_id}")
    #                 return None
                
    #             # Convert JSON fields back to Python objects
    #             result = {}
    #             for field, value in char_data.items():
    #                 try:
    #                     # Try to parse as JSON first
    #                     result[field] = json.loads(value)
    #                 except json.JSONDecodeError:
    #                     # If not JSON, keep as string (converted to appropriate type)
    #                     if value.isdigit():
    #                         result[field] = int(value)
    #                     elif value.replace('.', '', 1).isdigit():
    #                         result[field] = float(value)
    #                     else:
    #                         result[field] = value
                
    #             logger.debug(f"Retrieved character {character_id} for user {user_id} in battle {battle_id}")
    #             return result
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve character {character_id} for user {user_id}: {e}")
    #         return None
    
    # async def set_active_character(self, battle_id: int, user_id: int, character_id: int) -> bool:
    #     """
    #     Set which character is currently active for a user
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}:active")
                
    #             await redis_conn.setex(key, 1800, str(character_id))
                
    #             logger.debug(f"Set active character {character_id} for user {user_id} in battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to set active character for user {user_id}: {e}")
    #         return False
    
    # async def get_active_character(self, battle_id: int, user_id: int) -> Optional[int]:
    #     """
    #     Get the currently active character for a user
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             key = self._get_battle_key(battle_id, f"team:{user_id}:active")
                
    #             character_id_str = await redis_conn.get(key)
    #             if character_id_str is None:
    #                 logger.debug(f"No active character found for user {user_id} in battle {battle_id}")
    #                 return None
                
    #             character_id = int(character_id_str)
    #             logger.debug(f"Retrieved active character {character_id} for user {user_id} in battle {battle_id}")
    #             return character_id
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve active character for user {user_id}: {e}")
    #         return None
    
    # async def get_team_composition(self, battle_id: int, user_id: int) -> List[int]:
    #     """
    #     Get list of all character IDs in a user's team
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             # Pattern to match all character keys for this team
    #             pattern = self._get_battle_key(battle_id, f"team:{user_id}:character:*")
                
    #             # Get all matching keys
    #             character_keys = await redis_conn.keys(pattern)  # type: ignore
                
    #             # Extract character IDs from keys
    #             character_ids = []
    #             for key in character_keys:
    #                 # Key format: battle:{battle_id}:team:{user_id}:character:{character_id}
    #                 character_id = int(key.split(':')[-1])
    #                 character_ids.append(character_id)
                
    #             logger.debug(f"Retrieved {len(character_ids)} characters for user {user_id} in battle {battle_id}")
    #             return sorted(character_ids)
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve team composition for user {user_id}: {e}")
    #         return []
    
    # async def swap_active_character(self, battle_id: int, user_id: int, new_character_id: int) -> bool:
    #     """
    #     Atomically swap the active character and update swap cooldowns
    #     """
    #     try:
    #         redis_conn = await self.redis_manager.create_connection()
    #         try:
    #             pipe = redis_conn.pipeline()
                
    #             # Set new active character
    #             active_key = self._get_battle_key(battle_id, f"team:{user_id}:active")
    #             pipe.setex(active_key, 1800, str(new_character_id))
                
    #             # Set swap cooldown (prevent immediate swap back)
    #             cooldown_key = self._get_battle_key(battle_id, f"team:{user_id}:swap_cooldown")
    #             import time
    #             pipe.setex(cooldown_key, 1800, str(time.time()))
                
    #             # Add swap event to battle events
    #             event_key = self._get_battle_key(battle_id, "events")
    #             event_data = {
    #                 "type": "character_swap",
    #                 "user_id": user_id,
    #                 "new_character_id": new_character_id,
    #                 "timestamp": time.time()
    #             }
    #             pipe.rpush(event_key, json.dumps(event_data))
    #             pipe.expire(event_key, 1800)
                
    #             await pipe.execute()
                
    #             logger.debug(f"Swapped to character {new_character_id} for user {user_id} in battle {battle_id}")
    #             return True
    #         finally:
    #             await redis_conn.aclose()
                
    #     except Exception as e:
    #         logger.error(f"Failed to swap character for user {user_id}: {e}")
    #         return False
    
    # async def get_team_status(self, battle_id: int, user_id: int) -> Dict[str, Any]:
    #     """
    #     Get comprehensive team status including all characters and active character
    #     """
    #     try:
    #         # Get team composition
    #         character_ids = await self.get_team_composition(battle_id, user_id)
            
    #         # Get active character
    #         active_character_id = await self.get_active_character(battle_id, user_id)
            
    #         # Get data for each character
    #         characters = {}
    #         for char_id in character_ids:
    #             char_data = await self.get_character_in_team(battle_id, user_id, char_id)
    #             if char_data:
    #                 characters[char_id] = char_data
            
    #         team_status = {
    #             "user_id": user_id,
    #             "active_character_id": active_character_id,
    #             "team_size": len(character_ids),
    #             "characters": characters,
    #             "available_characters": [
    #                 char_id for char_id, data in characters.items()
    #                 if data.get("hp", 0) > 0
    #             ]
    #         }
            
    #         logger.debug(f"Retrieved team status for user {user_id} in battle {battle_id}")
    #         return team_status
            
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve team status for user {user_id}: {e}")
    #         return {}