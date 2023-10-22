from rest_framework import serializers, response
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=35, source="first_name")
    date_joined = serializers.DateTimeField(format="%m-%d-%Y")

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = ["username", "email", "password", "name", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    follower_count = serializers.SerializerMethodField("get_follower_count")
    following_count = serializers.SerializerMethodField("get_following_count")

    class Meta:
        model = UserProfile
        # fields = ["user", "date_of_birth"]
        extra_kwargs = {
            "followers": {"write_only": True},
            "following": {"write_only": True},
        }
        fields = "__all__"

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        follower_data = (
            validated_data.pop("followers") if "followers" in validated_data else []
        )
        following_data = (
            validated_data.pop("following") if "following" in validated_data else []
        )

        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        user_profile.followers.add(*follower_data)
        user_profile.following.add(*following_data)

        return user_profile
