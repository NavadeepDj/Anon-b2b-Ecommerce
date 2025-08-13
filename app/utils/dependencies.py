from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.core.redis_client import redis_client
import logging

logger = logging.getLogger(__name__)

# Security dependencies
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current user ID from JWT token
    """
    token = credentials.credentials
    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def get_optional_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    Dependency to get current user ID from JWT token (optional)
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    user_id = verify_token(token)
    return user_id


def get_redis() -> Generator:
    """
    Dependency to get Redis client
    """
    try:
        yield redis_client
    except Exception as e:
        logger.error(f"Redis connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cache service unavailable"
        )


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    return get_db()