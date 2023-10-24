from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.CharField(max_length=160, default="", blank=True)
    avatar = models.ImageField(null=True)
    cover_picture = models.ImageField(null=True)
    date_of_birth = models.DateField(max_length=10)

    def __str__(self) -> str:
        return self.user.username


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        UserProfile, related_name="following", on_delete=models.CASCADE
    )

    following_user_id = models.ForeignKey(
        UserProfile, related_name="followers", on_delete=models.CASCADE
    )

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)
