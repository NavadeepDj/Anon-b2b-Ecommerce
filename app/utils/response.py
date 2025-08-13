from typing import Any, Dict, Optional, Union
from fastapi import status
from fastapi.responses import JSONResponse
import time


class APIResponse:
    """Standardized API response utility"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
        meta: Optional[Dict[str, Any]] = None
    ) -> JSONResponse:
        """Create a successful response"""
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": time.time()
        }
        
        if meta:
            response_data["meta"] = meta
            
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> JSONResponse:
        """Create an error response"""
        response_data = {
            "success": False,
            "error": {
                "message": message,
                "code": error_code or f"HTTP_{status_code}",
                "timestamp": time.time()
            }
        }
        
        if details:
            response_data["error"]["details"] = details
            
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
    
    @staticmethod
    def validation_error(
        message: str = "Validation failed",
        errors: Optional[list] = None
    ) -> JSONResponse:
        """Create a validation error response"""
        return APIResponse.error(
            message=message,
            error_code="VALIDATION_ERROR",
            details=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        resource: Optional[str] = None
    ) -> JSONResponse:
        """Create a not found response"""
        error_message = f"{resource} not found" if resource else message
        return APIResponse.error(
            message=error_message,
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Authentication required"
    ) -> JSONResponse:
        """Create an unauthorized response"""
        return APIResponse.error(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(
        message: str = "Access forbidden"
    ) -> JSONResponse:
        """Create a forbidden response"""
        return APIResponse.error(
            message=message,
            error_code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def conflict(
        message: str = "Resource conflict",
        resource: Optional[str] = None
    ) -> JSONResponse:
        """Create a conflict response"""
        error_message = f"{resource} already exists" if resource else message
        return APIResponse.error(
            message=error_message,
            error_code="CONFLICT",
            status_code=status.HTTP_409_CONFLICT
        )
    
    @staticmethod
    def paginated(
        data: list,
        total: int,
        page: int = 1,
        per_page: int = 10,
        message: str = "Success"
    ) -> JSONResponse:
        """Create a paginated response"""
        total_pages = (total + per_page - 1) // per_page
        
        meta = {
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        return APIResponse.success(
            data=data,
            message=message,
            meta=meta
        )