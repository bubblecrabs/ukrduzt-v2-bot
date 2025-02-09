import json
from typing import Any

from redis.asyncio import Redis


class MailingService:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def publish(self, message: dict[str, Any]) -> None:
        """Publishes a message to the Redis channel."""
        await self.redis.publish("mailing_channel", json.dumps(message))

    async def subscribe(self) -> None:
        """Subscribes to the Redis channel and listens for messages."""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("mailing_channel")
