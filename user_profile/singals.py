from django.db.models.signals import post_delete
from .models import UserProfile


def userProfile_post_delete(sender, **kwargs):
    try:
        instance = kwargs["instance"]
        if instance.user:
            instance.user.delete()
    except:
        pass


post_delete.connect(userProfile_post_delete, UserProfile)
