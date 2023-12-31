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

    @property
    def name(self):
        return self.user.first_name

    def get_followers_in_common(self, otherUser: "UserProfile"):
        followers_in_common = (
            self.followers.all()
            .values_list("following_user_profile", flat=True)
            .intersection(
                otherUser.following.all().values_list("user_profile", flat=True)
            )
        )

        return followers_in_common

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

    def __str__(self) -> str:
        return f"{self.following_user_profile} follows {self.user_profile}"
