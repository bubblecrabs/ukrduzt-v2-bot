import json
from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis_url: str, ttl: int):
        """Initializes the Redis cache."""
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.ttl = ttl

    async def get(self, key: str):
        """Retrieves a cached value by key."""
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value, ttl: int = None):
        """Sets a value in the cache."""
        ttl = ttl or self.ttl
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def close(self):
        """Closes the Redis connection."""
        await self.redis.close()
