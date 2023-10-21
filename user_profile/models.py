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
    avatar = models.ImageField(null=True)
    cover_picture = models.ImageField(null=True)
    date_of_birth = models.DateField(max_length=10)
    following = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)

    def __str__(self) -> str:
        return self.user.username
