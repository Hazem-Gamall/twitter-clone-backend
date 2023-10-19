from rest_framework import serializers, response
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=35, source="first_name")

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = ["username", "email", "password", "name"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        # fields = ["user", "date_of_birth"]
        fields = "__all__"

    def create(self, validated_data):
        print("create")
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
