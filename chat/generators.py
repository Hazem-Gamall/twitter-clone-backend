from sse.generators import AsyncBaseGenerator
from .permissions import IsChatParticipant
from django.conf import settings


class ChatGenerator(AsyncBaseGenerator):
    permission_classes = [IsChatParticipant]
    channels = [settings.CHATS_CHANNEL]
