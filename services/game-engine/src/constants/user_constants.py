from enum import Enum

class UserOnboardResult(Enum):
    CREATED = "created"
    ALREADY_EXISTS = "already_exists"
    FAILED = "failed"
    NOT_FOUND = "not_found"
    
class UserConstants(Enum):
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    INVALID_REQUEST = "invalid_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    BAD_REQUEST = "bad_request"
    CONFLICT = "conflict"