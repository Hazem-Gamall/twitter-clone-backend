from rest_framework import serializers, response
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["date_of_birth"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    name = serializers.CharField(max_length=30, source="first_name")

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}, "profile": {}}
        fields = ["username", "email", "password", "name", "profile"]

    def create(self, validated_data):
        profile = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, date_of_birth=profile["date_of_birth"])
        return user
