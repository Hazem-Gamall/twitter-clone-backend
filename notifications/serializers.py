from rest_framework import serializers
from posts.serializers import PostSerializer
from user_profile.serializers import UserProfileSerializer
from .models import Notification


class NotificationsSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    issuer = UserProfileSerializer()
    receiver = UserProfileSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
