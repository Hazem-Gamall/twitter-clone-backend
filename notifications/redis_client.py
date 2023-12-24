from main import settings
from redis import asyncio as aioredis
import redis
from redis.exceptions import ConnectionError
from functools import cache
import json


@cache
def get_redis_client() -> redis.Redis:
    try:
        return redis.from_url(settings.REDIS_URL)
    except ConnectionError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


@cache
def get_async_redis_client() -> aioredis.Redis:
    try:
        return aioredis.from_url(settings.REDIS_URL)
    except ConnectionError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def send_notification(notification: dict):
    get_redis_client().publish(
        settings.PUSH_NOTIFICATIONS_CHANNEL, json.dumps(notification)
    )
