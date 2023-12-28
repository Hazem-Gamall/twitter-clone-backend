from rest_framework import serializers, response
from .models import UserProfile, UserFollowing, Mention
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from main.serializer_validation_mixins import ReadOnlyOrUnkownFieldErrorMixin
from main import settings


class MentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mention
        fields = ["user_profile", "post", "start_index", "end_index"]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=35, source="first_name")
    date_joined = serializers.DateTimeField(format="%m-%d-%Y", read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
        }
        fields = ["id", "username", "email", "password", "name", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    followed_by_user = serializers.SerializerMethodField("get_followed_by_user")
    followers_in_common = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ["liked_posts"]
        extra_fields = ["follower_count", "following_count"]

    def get_field_names(self, declared_fields, info):
        return super().get_field_names(declared_fields, info) + self.Meta.extra_fields

    def validate(self, attrs):
        if hasattr(self, "initial_data") and (
            "following" in self.initial_data or "followers" in self.initial_data
        ):
            raise ValidationError(
                {"following/followers": "You should use the dedicated endpoint"}
            )
        return super().validate(attrs)

    def get_followers_in_common(self, obj: UserProfile):
        if not "request" in self.context:
            return []
        auth_user_profile = self.context["request"].user.profile

        followers_in_common = obj.get_followers_in_common(auth_user_profile)
        count = followers_in_common.count()
        return {
            "users": UserProfileSerializer(
                UserProfile.objects.in_bulk((followers_in_common[:2])).values(),
                many=True,
            ).data,
            "count": count,
            "remaining": count - 2 if count > 2 else 0,
        }

    def get_followed_by_user(self, obj: UserProfile):
        if "request" in self.context:
            if not self.context["request"].user.is_authenticated:
                return False
            return obj.followers.filter(
                user_profile=obj,
                following_user_profile=self.context["request"].user.profile,
            ).exists()

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["avatar"] = f"{settings.MEDIA_URL}{data.get('avatar')}"
        data["cover_picture"] = f"{settings.MEDIA_URL}{data.get('cover_picture')}"
        return data


class UserFollowingSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = UserFollowing
        exclude = ["following_user_profile"]


class UserFollowersSerializer(serializers.ModelSerializer):
    following_user_profile = UserProfileSerializer()

    class Meta:
        model = UserFollowing
        exclude = ["user_profile"]
