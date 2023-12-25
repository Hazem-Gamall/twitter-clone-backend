from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from notifications.serializers import NotificationSerializer
from sse.redis_client import send_to_channel
from django.conf import settings


@receiver(post_save, sender="notifications.Notification")
def notification_handler(sender, **kwargs):
    if not kwargs["created"]:
        return
    notification = kwargs.pop("instance")
    send_to_channel(
        NotificationSerializer(notification).data, settings.PUSH_NOTIFICATIONS_CHANNEL
    )
