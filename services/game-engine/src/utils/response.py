from fastapi import FastAPI
from typing import Any

class APIResponse:
    """Utility class for standardizing API responses in FastAPI applications."""
    @staticmethod
    def success(data: Any, status_code: int = 200) -> tuple[Any, int]:
        return data, status_code
    
    @staticmethod
    def created(data:Any) -> tuple[Any,int]:
        return data,201
    
    @staticmethod
    def conflict(message: str = "Resource already exists") -> tuple[dict, int]:
        return {"error": message}, 409
    
    @staticmethod
    def not_found(message: str = "Resource not found") -> tuple[dict, int]:
        return {"error": message}, 404
    
    @staticmethod
    def error(message: str = "Request failed") -> tuple[dict, int]:
        return {"error": message}, 500
    
    @staticmethod
    def no_content(message: str = "No content") -> tuple[dict, int]:
        return {"No Content": message}, 204
    
    @staticmethod
    def already_exists(message: str = "Already Exists") -> tuple[dict, int]:
        return {"Already exists": message}, 204