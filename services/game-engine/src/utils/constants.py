from enum import Enum

class Constants(Enum):
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    INVALID_REQUEST = "invalid_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    BAD_REQUEST = "bad_request"
    CONFLICT = "conflict"
    CREATED = "created"
    ALREADY_EXISTS = "already_exists"
    FAILED = "failed"
    USER_NOT_FOUND = "user_not_found"
    NO_CONTENT = "no_content"