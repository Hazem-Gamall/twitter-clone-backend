from django.db import models
from user_profile.models import UserProfile


# Create your models here.
class Chat(models.Model):
    first_user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chat_set1"
    )
    second_user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="chat_set2"
    )

    creation = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["first_user_profile", "second_user_profile"]]


class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        UserProfile, related_name="messages", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creation"]
