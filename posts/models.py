from django.db import models
from main.abstract_models import ModelWithUser
from user_profile.models import UserProfile
from main.model_mixins import UpdatableModelMixin

# Create your models here.


class Post(ModelWithUser, UpdatableModelMixin):
    user = models.ForeignKey(UserProfile, models.CASCADE, related_name="posts")
    creation = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=280)
    repost = models.BooleanField(default=False)
    embed = models.ForeignKey(
        "self", models.CASCADE, null=True, blank=True, related_name="reposts"
    )
    reply_to = models.ForeignKey(
        "self", blank=True, on_delete=models.SET_NULL, null=True, related_name="replies"
    )

    def get_user(self):
        return self.user.user


from django.core.exceptions import ValidationError


def restrict_media(post_id):
    if Media.objects.filter(post_id=post_id).count() >= 6:
        raise ValidationError("A post can't have more than 6 media files")


class Media(models.Model):
    file = models.ImageField()
    post = models.ForeignKey(
        Post,
        related_name="media",
        validators=[restrict_media],
        on_delete=models.CASCADE,
        blank=True,
    )
