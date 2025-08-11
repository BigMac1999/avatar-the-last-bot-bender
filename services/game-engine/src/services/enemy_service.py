from repositories.enemy_repository import EnemyRepository
from fastapi import HTTPException, Response, status
from fastapi.responses import JSONResponse
from utils.constants import Constants
from typing import Any, Optional, List

import logging

logger = logging.getLogger(__name__)

class EnemyService:
    """
    Service class for enemy-related operations, including retrieval
    """
    enemy_repo = EnemyRepository()
    
    
    """Getter Methods"""