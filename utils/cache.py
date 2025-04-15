from functools import wraps
from typing import Any, Dict, Optional
import redis
import json
from datetime import timedelta

from ..config import settings
from .logging import logger

# Initialize Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

def cache_visualization(
    expiration: int = 3600,  # 1 hour default
    prefix: str = "viz"
) -> Any:
    """
    Cache decorator for visualization endpoints.
    
    Args:
        expiration (int): Cache expiration time in seconds
        prefix (str): Cache key prefix for the visualization type
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            cache_key = f"{prefix}:{kwargs.get('user_id')}:"
            cache_key += ":".join(f"{k}={v}" for k, v in sorted(kwargs.items())
                                if k != "db" and v is not None)
            
            # Try to get cached result
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    logger.info(f"Cache hit for key: {cache_key}")
                    return json.loads(cached_result)
                
                # Generate new result if not cached
                result = await func(*args, **kwargs)
                
                # Cache the result
                redis_client.setex(
                    cache_key,
                    expiration,
                    json.dumps(result)
                )
                logger.info(f"Cached result for key: {cache_key}")
                
                return result
                
            except redis.RedisError as e:
                logger.error(f"Redis error: {str(e)}")
                # Fall back to uncached result
                return await func(*args, **kwargs)
                
        return wrapper
    return decorator

def invalidate_user_cache(user_id: int, prefix: Optional[str] = None) -> None:
    """
    Invalidate all cached visualizations for a user.
    
    Args:
        user_id (int): The user ID
        prefix (str, optional): Specific visualization type to invalidate
    """
    try:
        pattern = f"{prefix}:{user_id}:*" if prefix else f"*:{user_id}:*"
        keys = redis_client.keys(pattern)
        
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache entries for user {user_id}")
            
    except redis.RedisError as e:
        logger.error(f"Error invalidating cache: {str(e)}")

def get_cache_stats() -> Dict[str, int]:
    """Get statistics about cached visualizations."""
    try:
        stats = {
            "total_cached": len(redis_client.keys("*")),
            "skill_network": len(redis_client.keys("viz:skill:*")),
            "timeline": len(redis_client.keys("viz:timeline:*")),
            "radar": len(redis_client.keys("viz:radar:*")),
            "goals": len(redis_client.keys("viz:goals:*"))
        }
        return stats
    except redis.RedisError as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return {"error": "Failed to get cache statistics"}