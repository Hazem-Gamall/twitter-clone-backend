from sse.generators import AsyncBaseGenerator
from .permissions import IsNotificationOwner
from django.conf import settings


class NotificationGenerator(AsyncBaseGenerator):
    permission_classes = [IsNotificationOwner]
    channels = [settings.PUSH_NOTIFICATIONS_CHANNEL]
