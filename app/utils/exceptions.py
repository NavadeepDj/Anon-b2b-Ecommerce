from typing import Any, Optional
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None,
        details: Optional[Any] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class ValidationException(BaseAPIException):
    """Exception for validation errors"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details
        )


class AuthenticationException(BaseAPIException):
    """Exception for authentication errors"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(BaseAPIException):
    """Exception for authorization errors"""
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundException(BaseAPIException):
    """Exception for resource not found errors"""
    
    def __init__(self, message: str = "Resource not found", resource: Optional[str] = None):
        error_message = f"{resource} not found" if resource else message
        super().__init__(
            message=error_message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND"
        )


class ConflictException(BaseAPIException):
    """Exception for resource conflict errors"""
    
    def __init__(self, message: str = "Resource conflict", resource: Optional[str] = None):
        error_message = f"{resource} already exists" if resource else message
        super().__init__(
            message=error_message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT"
        )


class BusinessLogicException(BaseAPIException):
    """Exception for business logic errors"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="BUSINESS_LOGIC_ERROR",
            details=details
        )


class ExternalServiceException(BaseAPIException):
    """Exception for external service errors"""
    
    def __init__(self, message: str = "External service error", service: Optional[str] = None):
        error_message = f"{service} service error: {message}" if service else message
        super().__init__(
            message=error_message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="EXTERNAL_SERVICE_ERROR"
        )


class RateLimitException(BaseAPIException):
    """Exception for rate limiting errors"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED"
        )


class DatabaseException(BaseAPIException):
    """Exception for database errors"""
    
    def __init__(self, message: str = "Database error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR"
        )


class CacheException(BaseAPIException):
    """Exception for cache errors"""
    
    def __init__(self, message: str = "Cache error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="CACHE_ERROR"
        )