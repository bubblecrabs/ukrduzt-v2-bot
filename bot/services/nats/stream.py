import asyncio

import nats
from nats.aio.client import Client
from nats.js.api import StreamConfig
from nats.js.client import JetStreamContext

from bot.core.config import settings


async def connect_to_nats(servers: str | list[str]) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(servers)
    js: JetStreamContext = nc.jetstream()
    return nc, js


async def subscribe_to_mailing(js: JetStreamContext):
    stream_config = StreamConfig(
        name="USER_NOTIFICATIONS",
        subjects=["notifications.mailing.*"]
    )
    await js.add_stream(stream_config)
    await js.subscribe("notifications.mailing.*")


async def main():
    nc, js = await connect_to_nats(settings.nats.url)
    await subscribe_to_mailing(js)
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
