"""
Battle State

Handles Redis operations for real-time battle state persistence and retrieval.
Manages temporary battle data during active combat sessions.
"""


class BattleState:
    
    def create_battle(self, battle_id: str, battle_data: dict):
        # TODO: Initialize new battle in Redis
        # TODO: Set battle metadata (created_at, status, etc.)
        # TODO: Store participant information
        pass
    
    def get_battle(self, battle_id: str):
        # TODO: Retrieve battle data from Redis
        # TODO: Return formatted battle state
        # TODO: Handle battle not found
        pass
    
    def update_battle(self, battle_id: str, updates: dict):
        # TODO: Update specific fields in Redis
        # TODO: Update last_modified timestamp
        # TODO: Handle partial updates
        pass
    
    def save_turn_data(self, battle_id: str, turn_data: dict):
        # TODO: Append turn data to battle history
        # TODO: Update current turn number
        # TODO: Save participant state changes
        pass
    
    def delete_battle(self, battle_id: str):
        # TODO: Remove battle from Redis
        # TODO: Clean up any related keys
        # TODO: Return success/failure
        pass
    
    def get_all_active_battles(self):
        # TODO: Get list of all active battles
        # TODO: Filter by status if needed
        # TODO: Return battle summaries
        pass

import json
import logging
from typing import Optional, Dict, Any, List
from database.connection import redis_manager

logger = logging.getLogger(__name__)


class BattleStateCache:
    """
    High-level interface for battle state caching operations
    
    This class provides battle-specific caching methods while abstracting
    away the Redis implementation details. It handles:
    - JSON serialization/deserialization
    - Key naming conventions
    - TTL (Time To Live) management
    - Error handling
    """
    
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
    
    async def set_battle_state(self, battle_id: int, state_data: Dict[str, Any], ttl: int = 1800) -> bool:
        """
        Store complete battle state in Redis
        
        Args:
            battle_id: Unique battle identifier
            state_data: Python dictionary containing battle state
            ttl: Time To Live in seconds (1800 = 30 minutes)
            
        Returns:
            True if successful, False otherwise
            
        Redis Concepts:
        - JSON serialization: Convert Python dict to JSON string for storage
        - TTL: Automatic expiration prevents Redis from filling up with old data
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, "state")
                
                # Convert Python dictionary to JSON string
                # Redis stores strings, not Python objects
                json_data = json.dumps(state_data)
                
                # Store with expiration time (TTL)
                # setex = SET with EXpiration
                await redis_conn.setex(key, ttl, json_data)
                
                logger.debug(f"Stored battle state for battle {battle_id}")
                return True
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to store battle state for battle {battle_id}: {e}")
            return False
    
    async def get_battle_state(self, battle_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve battle state from Redis
        
        Returns:
            Dictionary containing battle state, or None if not found/error
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, "state")
                
                # Get JSON string from Redis
                json_data = await redis_conn.get(key)
                
                if json_data is None:
                    logger.debug(f"No battle state found for battle {battle_id}")
                    return None
                
                # Convert JSON string back to Python dictionary
                # Redis returns string due to decode_responses=True
                state_data = json.loads(str(json_data))
                logger.debug(f"Retrieved battle state for battle {battle_id}")
                return state_data
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to retrieve battle state for battle {battle_id}: {e}")
            return None
    
    async def delete_battle_state(self, battle_id: int) -> bool:
        """
        Remove battle state from Redis (cleanup after battle ends)
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, "state")
                
                # Delete the key - returns number of keys deleted
                deleted_count = await redis_conn.delete(key)
                
                if deleted_count > 0:
                    logger.debug(f"Deleted battle state for battle {battle_id}")
                    return True
                else:
                    logger.debug(f"No battle state to delete for battle {battle_id}")
                    return False
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to delete battle state for battle {battle_id}: {e}")
            return False
    
    async def set_participant_data(self, battle_id: int, participant_id: int, participant_data: Dict[str, Any]) -> bool:
        """
        Store participant data using Redis Hash
        
        Redis Hashes are perfect for storing object-like data (like participant info)
        Instead of storing everything as JSON, we can store individual fields
        
        Benefits of Redis Hashes:
        - Can update individual fields without rewriting entire object
        - More memory efficient for structured data
        - Built-in commands for hash operations
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, f"participant:{participant_id}")
                
                # Convert nested objects to JSON, keep simple values as-is
                hash_data = {}
                for field, value in participant_data.items():
                    if isinstance(value, (dict, list)):
                        # Complex data structures need to be JSON serialized
                        hash_data[field] = json.dumps(value)
                    else:
                        # Simple values can be stored directly
                        hash_data[field] = str(value)
                
                # Store as Redis hash with TTL
                # hset = Hash SET (set multiple hash fields at once)
                await redis_conn.hset(key, mapping=hash_data)  # type: ignore
                await redis_conn.expire(key, 1800)  # Set TTL separately for hashes
                
                logger.debug(f"Stored participant {participant_id} data for battle {battle_id}")
                return True
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to store participant data: {e}")
            return False
    
    async def add_battle_event(self, battle_id: int, event_data: Dict[str, Any]) -> bool:
        """
        Add event to battle event log using Redis Lists
        
        Redis Lists are perfect for:
        - Event logs (append-only)
        - Action queues
        - History tracking
        
        Lists maintain order and support efficient push/pop operations
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, "events")
                
                # Add timestamp to event
                import time
                event_data['timestamp'] = time.time()
                
                # Convert to JSON and add to list
                event_json = json.dumps(event_data)
                
                # lpush = Left PUSH (add to beginning of list)
                # rpush = Right PUSH (add to end of list)
                # We use rpush to maintain chronological order
                await redis_conn.rpush(key, event_json)  # type: ignore
                
                # Set TTL if this is the first event (key didn't exist)
                await redis_conn.expire(key, 1800)
                
                logger.debug(f"Added event to battle {battle_id}")
                return True
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to add battle event: {e}")
            return False
    
    async def get_battle_events(self, battle_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent battle events using Redis List operations
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = self._get_battle_key(battle_id, "events")
                
                # lrange = List RANGE (get slice of list)
                # -limit to -1 gets the last 'limit' items
                event_strings = await redis_conn.lrange(key, -limit, -1)  # type: ignore
                
                # Convert JSON strings back to Python objects
                events = []
                for event_str in event_strings:
                    try:
                        event_data = json.loads(event_str)
                        events.append(event_data)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in battle event: {event_str}")
                        continue
                
                logger.debug(f"Retrieved {len(events)} events for battle {battle_id}")
                return events
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to retrieve battle events: {e}")
            return []
    
    async def execute_battle_transaction(self, battle_id: int, updates: Dict[str, Any]) -> bool:
        """
        Execute multiple Redis operations atomically using transactions
        
        Redis Transactions (MULTI/EXEC):
        - Group multiple commands together
        - Execute all commands atomically (all succeed or all fail)
        - Prevent race conditions in concurrent environments
        
        Example use case: When a player makes a move, we need to:
        1. Update battle state
        2. Add event to log  
        3. Update participant data
        4. Set battle as modified
        
        All of these should happen together or not at all.
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                # Start Redis transaction
                # pipeline() creates a transaction context
                pipe = redis_conn.pipeline()
                
                # Add commands to transaction (they don't execute yet)
                
                # 1. Update battle state
                if 'state' in updates:
                    state_key = self._get_battle_key(battle_id, "state")
                    state_json = json.dumps(updates['state'])
                    pipe.setex(state_key, 1800, state_json)
                
                # 2. Add event if provided
                if 'event' in updates:
                    event_key = self._get_battle_key(battle_id, "events")
                    event_data = updates['event']
                    import time
                    event_data['timestamp'] = time.time()
                    event_json = json.dumps(event_data)
                    pipe.rpush(event_key, event_json)
                    pipe.expire(event_key, 1800)
                
                # 3. Update participant data if provided
                if 'participants' in updates:
                    for participant_id, participant_data in updates['participants'].items():
                        participant_key = self._get_battle_key(battle_id, f"participant:{participant_id}")
                        
                        # Convert data for hash storage
                        hash_data = {}
                        for field, value in participant_data.items():
                            if isinstance(value, (dict, list)):
                                hash_data[field] = json.dumps(value)
                            else:
                                hash_data[field] = str(value)
                        
                        pipe.hset(participant_key, mapping=hash_data)
                        pipe.expire(participant_key, 1800)
                
                # 4. Set last modified timestamp
                modified_key = self._get_battle_key(battle_id, "modified")
                import time
                pipe.setex(modified_key, 1800, str(time.time()))
                
                # Execute all commands atomically
                # execute() runs all commands in the pipeline together
                results = await pipe.execute()
                
                logger.debug(f"Executed transaction for battle {battle_id} with {len(results)} operations")
                return True
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to execute battle transaction: {e}")
            return False
    
    async def get_active_battles_for_user(self, user_id: int) -> List[int]:
        """
        Get list of active battles for a user using Redis Sets
        
        Redis Sets are perfect for:
        - Storing unique items (no duplicates)
        - Fast membership testing
        - Set operations (union, intersection, difference)
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = f"active_battles:user:{user_id}"
                
                # smembers = Set MEMBERS (get all items in set)
                battle_ids_str = await redis_conn.smembers(key)  # type: ignore
                
                # Convert strings back to integers
                battle_ids = [int(bid) for bid in battle_ids_str]
                
                logger.debug(f"Found {len(battle_ids)} active battles for user {user_id}")
                return battle_ids
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to get active battles for user {user_id}: {e}")
            return []
    
    async def add_user_to_active_battle(self, user_id: int, battle_id: int) -> bool:
        """
        Add user to active battles set
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = f"active_battles:user:{user_id}"
                
                # sadd = Set ADD (add item to set)
                await redis_conn.sadd(key, battle_id)  # type: ignore
                await redis_conn.expire(key, 7200)  # 2 hours TTL for active battle tracking
                
                logger.debug(f"Added user {user_id} to active battle {battle_id}")
                return True
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to add user to active battle: {e}")
            return False
    
    async def remove_user_from_active_battle(self, user_id: int, battle_id: int) -> bool:
        """
        Remove user from active battles set
        """
        try:
            redis_conn = await self.redis_manager.create_connection()
            try:
                key = f"active_battles:user:{user_id}"
                
                # srem = Set REMove (remove item from set)
                removed_count = await redis_conn.srem(key, battle_id)  # type: ignore
                
                if removed_count > 0:
                    logger.debug(f"Removed user {user_id} from active battle {battle_id}")
                    return True
                else:
                    logger.debug(f"User {user_id} was not in active battle {battle_id}")
                    return False
            finally:
                await redis_conn.aclose()
                
        except Exception as e:
            logger.error(f"Failed to remove user from active battle: {e}")
            return False