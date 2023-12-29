from typing import Callable, AsyncGenerator, List
import json
from rest_framework.permissions import BasePermission
from django.conf import settings
from .redis_client import get_async_redis_client
from datetime import datetime


class AsyncBaseGenerator:
    def __init__(self, request) -> None:
        self.redis_client = get_async_redis_client()
        self.attrs = type(self)._get_attributes()
        self.request = request

    @staticmethod
    def _get_class_attributes(cls):
        attrs = {}
        for key in cls.__dict__.keys():
            if key.startswith("__") or key.startswith("_"):
                continue
            attrs[key] = getattr(cls, key)
        return attrs

    @classmethod
    def _get_attributes(cls):
        attrs = {}
        for base in cls.__bases__:
            attrs.update(cls._get_class_attributes(base))
        attrs.update(cls._get_class_attributes(cls))
        if "channels" not in attrs:
            raise Exception("you need to provide the channels to listen to")
        return attrs

    def generate_response(self, message):
        return f"data: {json.dumps(message)}\n\n"

    def get_permessions(self) -> List[BasePermission]:
        return [permission() for permission in self.attrs["permission_classes"]]

    def check_permessions(self, obj) -> bool:
        permessions = self.get_permessions()
        for permession in permessions:
            if not permession.has_object_permission(self.request, obj=obj):
                return False
        return True

    async def get_generator(self) -> AsyncGenerator:
        async with self.redis_client.pubsub() as listener:
            await listener.subscribe(*self.attrs["channels"])
            is_on_connect = True

            while True:
                message = await listener.get_message(
                    timeout=settings.PUSH_NOTIFICATIONS_DELAY_SECONDS,
                    ignore_subscribe_messages=True,
                )

                if message is None:
                    message = {"ping": datetime.now()}
                    yield f"data: {json.dumps(message, default=str)}\n\n"
                    continue

                message = json.loads(message["data"])
                if self.check_permessions(message):
                    yield self.generate_response(message=message)
