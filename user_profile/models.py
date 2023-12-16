from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from main.abstract_models import ModelWithUser

# Create your models here.


class UserProfile(ModelWithUser):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.CharField(max_length=160, default="", blank=True)
    avatar = models.ImageField(null=True)
    cover_picture = models.ImageField(null=True)
    date_of_birth = models.DateField(max_length=10)
    liked_posts = models.ManyToManyField("posts.Post", related_name="likes")

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def chats(self):
        return self.chat_set1.all() | self.chat_set2.all()

    def get_user(self):
        return self.user

    def __str__(self) -> str:
        return self.user.username


class Mention(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, related_name="user_mentions", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "posts.Post", related_name="post_mentions", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    start_index = models.IntegerField()
    end_index = models.IntegerField()


class UserFollowing(models.Model):
    class Meta:
        unique_together = [["user_profile", "following_user_profile"]]

    # the profile to be followed
    user_profile = models.ForeignKey(
        UserProfile, related_name="followers", on_delete=models.CASCADE
    )

    # the profile making the follow
    following_user_profile = models.ForeignKey(
        UserProfile, related_name="following", on_delete=models.CASCADE
    )

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        REPLY = "R", "Reply"
        REPOST = "T", "Repost"
        LIKE = "L", "Like"
        MENTION = "M", "Mention"

    notification_type = models.CharField(
        choices=NotificationType.choices, blank=False, null=False, max_length=1
    )
    issuer = models.ForeignKey(UserProfile, models.CASCADE)
    reciever = models.ForeignKey(
        UserProfile, models.CASCADE, related_name="notifications"
    )
    creation = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
