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
    date_of_birth = models.DateField(max_length=8)
    following = models.ManyToManyField("self")
    followers = models.ManyToManyField("self")
