from typing import Callable, AsyncGenerator
import json
from main import settings
from .redis_client import get_async_redis_client
from datetime import datetime


async def listen_to_channel(filter_func: Callable, user_id: int) -> AsyncGenerator:
    # Create message listener and subscribe on the event source channel
    async with get_async_redis_client().pubsub() as listener:
        await listener.subscribe(settings.PUSH_NOTIFICATIONS_CHANNEL)
        is_on_connect = True
        # Create a generator that will 'yield' our data into opened connection
        while True:
            message = await listener.get_message(
                timeout=settings.PUSH_NOTIFICATIONS_DELAY_SECONDS,
                ignore_subscribe_messages=True,
            )
            print("message here", message)
            # Send on connect message
            if message is None and is_on_connect:
                yield ""
                is_on_connect = False
                continue
            # Send heartbeat message
            if message is None and not is_on_connect:
                message = {"ping": datetime.now()}
                # yield f"data: {json.dumps(message, default=str)}\n\n"
                yield ""
                continue
            message = json.loads(message["data"])
            # Check if the authorized user is a recipient of the notification
            if filter_func(user_id, message):
                print("sending message")
                yield f"data: {json.dumps(message)}\n\n"
