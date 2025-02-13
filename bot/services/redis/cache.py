import json
from collections.abc import Callable, Coroutine
from functools import wraps

from bot.core.config import settings
from bot.core.loader import storage


def cache_response(cache_key_template: str) -> Callable[[Callable[..., Coroutine]], Callable[..., Coroutine]]:
    """A decorator for caching results of asynchronous functions in Redis."""
    def decorator(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = cache_key_template.format(**kwargs)
            cached_data = await storage.redis.get(name=cache_key)
            if cached_data:
                return json.loads(cached_data)

            result = await func(*args, **kwargs)
            if result is not None:
                await storage.redis.setex(name=cache_key, time=settings.redis.ttl, value=json.dumps(result))
            return result
        return wrapper
    return decorator
