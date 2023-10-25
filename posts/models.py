from django.db import models
from user_profile.models import UserProfile
from main.model_mixins import UpdatableModelMixin

# Create your models here.


class Post(models.Model, UpdatableModelMixin):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name="posts")
    creation = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=280)
    repost = models.BooleanField(default=False)
    embed = models.ForeignKey(
        "self", models.SET_NULL, null=True, blank=True, related_name="reposts"
    )
    replies = models.ManyToManyField("self", blank=True)


from django.core.exceptions import ValidationError


def restrict_media(post_id):
    if Media.objects.filter(post_id=post_id).count() >= 6:
        raise ValidationError("A post can't have more than 6 media files")


class Media(models.Model):
    file = models.FileField()
    post = models.ForeignKey(
        Post,
        related_name="media",
        validators=[restrict_media],
        on_delete=models.CASCADE,
        blank=True,
    )
