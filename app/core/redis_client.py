import redis
from app.core.config import settings
import logging
import json
from typing import Any, Optional

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis_client = None
        self.connect()
    
    def connect(self):
        """
        Initialize Redis connection
        """
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from Redis
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Set value in Redis with optional expiration
        """
        try:
            serialized_value = json.dumps(value)
            result = self.redis_client.set(key, serialized_value, ex=expire)
            return result
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete key from Redis
        """
        try:
            result = self.redis_client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis
        """
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking existence of key {key} in Redis: {e}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration for a key
        """
        try:
            return bool(self.redis_client.expire(key, seconds))
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False
    
    def flushdb(self) -> bool:
        """
        Clear all keys in current database (use with caution)
        """
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Error flushing Redis database: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()