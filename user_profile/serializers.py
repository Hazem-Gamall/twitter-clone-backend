from rest_framework import serializers, response
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from main.serializer_validation_mixins import ReadOnlyOrUnkownFieldErrorMixin


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=35, source="first_name")
    date_joined = serializers.DateTimeField(format="%m-%d-%Y", read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
        }
        fields = ["username", "email", "password", "name", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    follower_count = serializers.SerializerMethodField("get_follower_count")
    following_count = serializers.SerializerMethodField("get_following_count")

    class Meta:
        model = UserProfile
        fields = "__all__"

    def validate(self, attrs):
        if hasattr(self, "initial_data") and (
            "following" in self.initial_data or "followers" in self.initial_data
        ):
            raise ValidationError(
                {"following/followers": "You should use the dedicated endpoint"}
            )
        return super().validate(attrs)

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop("user")

        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)

        return user_profile

    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_data["name"] = user_data.get("first_name", instance.user.first_name)
            updated_user = UserSerializer(
                instance.user, user_data, partial=self.partial
            )
            if updated_user.is_valid():
                updated_user.save()

        return super().update(instance, validated_data)
