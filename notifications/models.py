from django.db import models
from user_profile.models import UserProfile
from posts.models import Post
from main.abstract_models import ModelWithUser

# Create your models here.


class Notification(ModelWithUser):
    class NotificationType(models.TextChoices):
        REPLY = "R", "Reply"
        REPOST = "T", "Repost"
        LIKE = "L", "Like"
        MENTION = "M", "Mention"

    notification_type = models.CharField(
        choices=NotificationType.choices, blank=False, null=False, max_length=1
    )
    issuer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        UserProfile, models.CASCADE, related_name="notifications"
    )
    creation = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def get_user(self):
        return self.receiver.user

    class Meta:
        ordering = ["-creation"]
