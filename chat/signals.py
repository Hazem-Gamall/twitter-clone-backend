from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from chat.serializers import RetrieveMessageSerializer
from sse.redis_client import send_to_channel
from django.conf import settings


@receiver(post_save, sender="chat.Message")
def message_handler(sender, **kwargs):
    if not kwargs["created"]:
        return
    message = kwargs.pop("instance")
    send_to_channel(RetrieveMessageSerializer(message).data, settings.CHATS_CHANNEL)
