import os
import json
import redis
from typing import Optional, Any

class CacheService:
    """
    Redis caching service for match scores and repeated queries.
    """

    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        print(f"Connected to Redis at {redis_url}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache.
        """
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, expire: int = 3600):
        """
        Sets a value in the cache with an expiration time (default 1 hour).
        """
        self.redis_client.set(key, json.dumps(value), ex=expire)

    def delete(self, key: str):
        """
        Removes a key from the cache.
        """
        self.redis_client.delete(key)
